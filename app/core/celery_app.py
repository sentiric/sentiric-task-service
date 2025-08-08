from celery import Celery
from app.core.config import settings
from app.core.logging import setup_logging # YENİ

# YENİ: Celery worker başladığında loglamayı ayarla
setup_logging()

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.example_tasks"] # Görevlerin nerede olduğunu belirtiyoruz
)

celery_app.conf.update(
    task_track_started=True,
)