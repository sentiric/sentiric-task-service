from celery import Celery
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.example_tasks", "app.tasks.guardian_tasks"]
)

celery_app.conf.update(
    task_track_started=True,
    # YENİ: Eğer REDIS_USE_SSL true ise, Celery'e SSL ayarlarını bildir.
    redis_backend_use_ssl={'ssl_cert_reqs': None} if settings.REDIS_USE_SSL else None,
    broker_use_ssl={'ssl_cert_reqs': None} if "amqps" in settings.RABBITMQ_URL else None,
)

celery_app.conf.beat_schedule = {
    'keep-services-alive-every-4-minutes': {
        'task': 'app.tasks.guardian_tasks.keep_services_alive',
        'schedule': 240.0,
    },
}