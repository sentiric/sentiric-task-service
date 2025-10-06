# sentiric-task-service/app/core/celery_app.py
from celery import Celery
from app.core.config import settings

# Celery uygulamasını Broker ve Backend URL'leri ile oluştur
celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    # Hangi task modüllerini otomatik olarak yükleyeceğini belirt
    include=["app.tasks.example_tasks", "app.tasks.guardian_tasks"] 
)

# Celery Ayarları
celery_app.conf.update(
    task_track_started=True, # Görevlerin STARTED durumunu raporlamasını sağlar
    broker_connection_retry_on_startup=True,
    broker_transport_options={
        'max_retries': 10,
        'interval_start': 0,
        'interval_step': 0.5,
        'interval_max': 5
    }
)

# Celery Beat (Zamanlanmış Görevler) Ayarları
celery_app.conf.beat_schedule = {
    'platform-guardian-ping-services': {
        'task': 'app.tasks.guardian_tasks.ping_external_services',
        # Her 4 dakikada bir (240 saniye) çalıştır (Bulut servislerinin uyumasını engellemek için)
        'schedule': 240.0, 
    },
}