from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.example_tasks", "app.tasks.guardian_tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    # YENİ: Dinamik olarak oluşturulan SSL opsiyonlarını ekle
    broker_transport_options=settings.CELERY_BROKER_OPTIONS,
    redis_backend_transport_options=settings.CELERY_REDIS_BACKEND_OPTIONS,
)

celery_app.conf.beat_schedule = {
    'platform-guardian-ping-services': {
        'task': 'app.tasks.guardian_tasks.ping_external_services',
        'schedule': 240.0,
    },
}