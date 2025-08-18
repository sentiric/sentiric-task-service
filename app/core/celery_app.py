from celery import Celery
from app.core.config import settings

# --- KRİTİK DÜZELTME BURADA ---
# SSL ayarlarını doğrudan Celery uygulamasını oluştururken parametre olarak veriyoruz.
# Bu, ayarların en erken ve en doğru zamanda yüklenmesini garanti eder.
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.example_tasks", "app.tasks.guardian_tasks"],
    broker_transport_options=settings.CELERY_BROKER_OPTIONS,
    result_backend_transport_options=settings.CELERY_REDIS_BACKEND_OPTIONS
)

# Diğer ayarları .conf.update ile yapmaya devam edebiliriz.
celery_app.conf.update(
    task_track_started=True,
)

celery_app.conf.beat_schedule = {
    'platform-guardian-ping-services': {
        'task': 'app.tasks.guardian_tasks.ping_external_services',
        'schedule': 240.0,
    },
}