import structlog # YENİ
from app.core.celery_app import celery_app
from app.core.config import settings
import psycopg2
import redis
from qdrant_client import QdrantClient
from urllib.parse import urlparse

# DÜZELTME: Logger'ı doğrudan structlog'dan alıyoruz.
logger = structlog.get_logger(__name__)

@celery_app.task(acks_late=True, name="app.tasks.guardian_tasks.keep_services_alive")
def keep_services_alive():
    """
    Ücretsiz bulut servislerinin "uykuya dalmasını" veya "pasiflik nedeniyle silinmesini"
    önlemek için periyodik olarak hepsine basit birer istek atar.
    """
    logger.info("Platform Guardian: Servisleri aktif tutma görevi başlatıldı.")
    
    # 1. PostgreSQL (Neon) Ping
    try:
        conn = psycopg2.connect(settings.POSTGRES_URL)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        logger.info("Platform Guardian: PostgreSQL (Neon) başarıyla pinglendi.")
    except Exception as e:
        logger.error("Platform Guardian: PostgreSQL (Neon) pinglenirken hata oluştu.", error=str(e))

    # 2. Redis (Upstash / Yerel) Ping
    try:
        # DÜZELTME: Artık SSL'i dinamik olarak kontrol ediyoruz.
        if settings.REDIS_USE_SSL:
            r = redis.from_url(settings.REDIS_URL)
        else:
            r = redis.from_url(settings.REDIS_URL) # from_url zaten `redis://` için doğru çalışır.
        
        r.ping()
        logger.info("Platform Guardian: Redis başarıyla pinglendi.", use_ssl=settings.REDIS_USE_SSL)
    except Exception as e:
        logger.error("Platform Guardian: Redis pinglenirken hata oluştu.", error=str(e))

    # 3. Qdrant Ping
    try:
        # DÜZELTME: Artık https parametresini konfigürasyondan dinamik olarak alıyoruz.
        client = QdrantClient(
            host=settings.VECTOR_DB_HOST,
            port=settings.VECTOR_DB_PORT,
            api_key=settings.QDRANT_API_KEY,
            https=settings.VECTOR_DB_USE_HTTPS # <-- Burası kritik!
        )
        client.get_collections()
        logger.info("Platform Guardian: Qdrant başarıyla pinglendi.", use_https=settings.VECTOR_DB_USE_HTTPS)
    except Exception as e:
        logger.error("Platform Guardian: Qdrant pinglenirken hata oluştu.", error=str(e))
        
    return "All free-tier services have been pinged."