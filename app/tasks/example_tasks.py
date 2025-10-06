# sentiric-task-service/app/tasks/example_tasks.py
from app.core.celery_app import celery_app
import time

@celery_app.task(acks_late=True)
def long_running_task(x: int, y: int) -> int:
    """API tarafından tetiklenen basit bir toplama ve bekleme görevi."""
    time.sleep(5) # 5 saniye bekleme simülasyonu
    return x + y