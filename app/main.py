from fastapi import FastAPI
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import Any
from contextlib import asynccontextmanager # YENİ
from prometheus_fastapi_instrumentator import Instrumentator # YENİ
from app.core.logging import setup_logging # YENİ

from app.core.celery_app import celery_app
from app.tasks.example_tasks import long_running_task

# YENİ: Lifespan ile başlangıçta loglamayı ayarlama
@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield

app = FastAPI(title="Sentiric Task Service", lifespan=lifespan)

# YENİ: Prometheus metriklerini ekle
Instrumentator().instrument(app).expose(app)

class TaskRequest(BaseModel):
    x: int
    y: int

class TaskResponse(BaseModel):
    task_id: str
    status: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    # YENİ: 'result' alanını daha esnek olan 'Any' tipiyle tanımlıyoruz.
    # Bu, Celery'den gelebilecek her türlü sonucu kabul etmemizi sağlar.
    result: Any | None = None



# YENİ: Healthcheck endpoint'i
@app.get("/health", tags=["Health"])
def health_check():
    try:
        # Celery worker'larının en az birinin hayatta olup olmadığını kontrol et
        i = celery_app.control.inspect()
        stats = i.stats()
        if not stats:
            return {"status": "degraded", "detail": "No running workers found."}
        return {"status": "ok", "workers_online": list(stats.keys())}
    except Exception as e:
        return {"status": "error", "detail": f"Cannot connect to broker: {str(e)}"}


@app.post("/api/v1/tasks/long_task", response_model=TaskResponse, status_code=202)
def run_long_task(request: TaskRequest):
    """Uzun süren bir görevi arka planda çalıştırmak için tetikler."""
    task = long_running_task.delay(request.x, request.y)
    return {"task_id": task.id, "status": "PENDING"}

@app.get("/api/v1/tasks/status/{task_id}", response_model=TaskStatus)
def get_task_status(task_id: str):
    """Verilen bir task_id'nin durumunu ve sonucunu sorgular."""
    task_result = AsyncResult(task_id, app=celery_app)
    result = None

    if task_result.ready():
        if task_result.successful():
            result = task_result.get() # .result yerine .get() kullanmak daha güvenlidir.
        else:
            # Hata durumunda, hatayı string olarak alalım.
            try:
                # task_result.get() hata fırlatabilir, bunu yakalayalım.
                result = str(task_result.get(propagate=False))
            except Exception as e:
                result = f"Görevin sonucunu alırken hata oluştu: {str(e)}"
    
    # --- KRİTİK DÜZELTME ---
    # Eğer görev henüz hazır değilse, sonucu None olarak bırak.
    # Bu, "Internal Server Error" hatasını önler.
    if task_result.status == 'PENDING':
        result = "Task is still running."

    return {"task_id": task_id, "status": task_result.status, "result": result}