from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from typing import Any # <-- YENİ IMPORT

from app.core.celery_app import celery_app
from app.tasks.example_tasks import long_running_task

app = FastAPI(title="Sentiric Task Service")

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