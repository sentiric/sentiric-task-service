# sentiric-task-service/app/main.py
from fastapi import FastAPI, status
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import Any
from contextlib import asynccontextmanager 
from prometheus_fastapi_instrumentator import Instrumentator 
from app.core.logging import setup_logging 

from app.core.celery_app import celery_app
from app.tasks.example_tasks import long_running_task
import structlog

logger = structlog.get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("Task Service API başlatılıyor")
    
    # Prometheus metriklerini ekle
    Instrumentator().instrument(app).expose(app)
    
    yield

app = FastAPI(title="Sentiric Task Service API", lifespan=lifespan)

class TaskRequest(BaseModel):
    x: int
    y: int

class TaskResponse(BaseModel):
    task_id: str
    status: str

class TaskStatus(BaseModel):
    task_id: str
    status: str
    result: Any | None = None


# --- Healthcheck endpoint'i (Broker ve Worker durumu dahil) ---
@app.get("/health", tags=["Health"])
def health_check():
    try:
        i = celery_app.control.inspect()
        stats = i.stats()
        
        # Eğer stats boşsa (Celery broker'a bağlanamıyordur veya worker yok)
        if not stats:
            logger.warning("Celery: Worker istatistikleri alınamadı.")
            return {"status": "degraded", "detail": "No running workers or cannot connect to broker."}
        
        return {"status": "ok", "workers_online": list(stats.keys())}
    except Exception as e:
        logger.error("Celery broker bağlantı hatası", error=str(e))
        return {"status": "error", "detail": f"Cannot connect to Celery broker: {str(e)}"}


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
            result = task_result.get()
        else:
            result = str(task_result.info) # Hata durumunda hata bilgisini al
    elif task_result.status == 'PENDING':
        result = "Task is still queued or running."

    return {"task_id": task_id, "status": task_result.status, "result": result}