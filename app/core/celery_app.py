from celery import Celery
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.example_tasks", "app.tasks.guardian_tasks"] # YENİ: Yeni görev dosyamızı ekliyoruz
)

celery_app.conf.update(
    task_track_started=True,
)

# YENİ: Her 4 dakikada bir "Platform Bekçisi" görevini çalıştıracak zamanlama
celery_app.conf.beat_schedule = {
    'keep-services-alive-every-4-minutes': {
        'task': 'app.tasks.guardian_tasks.keep_services_alive',
        'schedule': 240.0,  # saniye cinsinden (4 dakika)
    },
}