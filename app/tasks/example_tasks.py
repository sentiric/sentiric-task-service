from app.core.celery_app import celery_app
import time

@celery_app.task(acks_late=True)
def long_running_task(x: int, y: int) -> int:
    """5 saniye uyuyan ve iki sayıyı toplayan basit bir görev."""
    time.sleep(5)
    return x + y