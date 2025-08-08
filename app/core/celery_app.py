from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.example_tasks"] # Görevlerin nerede olduğunu belirtiyoruz
)

celery_app.conf.update(
    task_track_started=True,
)