import httpx
import asyncio
import structlog
from app.core.celery_app import celery_app
from app.core.config import settings

logger = structlog.get_logger(__name__)

# Uyanık tutulacak servislerin listesi
# .env.generated dosyasından bu URL'ler gelecek.
EXTERNAL_SERVICES = [
    settings.LLM_SERVICE_URL,
    settings.STT_SERVICE_URL,
    settings.TTS_EDGE_SERVICE_URL,
    settings.KNOWLEDGE_SERVICE_URL,
]

async def ping_service(client: httpx.AsyncClient, service_name: str, url: str):
    """Tek bir servisin /health endpoint'ine istek atar."""
    try:
        health_url = f"{url.rstrip('/')}/health"
        response = await client.get(health_url, timeout=30.0)
        if response.status_code == 200:
            logger.info("Platform Guardian: Servis başarıyla pinglendi.", service=service_name, status="ok")
        else:
            logger.warning("Platform Guardian: Servis uyarı durumu döndürdü.", service=service_name, status_code=response.status_code)
    except httpx.RequestError as e:
        logger.error("Platform Guardian: Servise ulaşılamadı.", service=service_name, error=str(e))

async def ping_all_services():
    """Tüm harici servisleri asenkron olarak pingler."""
    async with httpx.AsyncClient() as client:
        tasks = []
        for url in EXTERNAL_SERVICES:
            # URL'den servis adını çıkarmak için basit bir mantık
            service_name = url.split('.')[0].split('//')[-1]
            tasks.append(ping_service(client, service_name, url))
        await asyncio.gather(*tasks)

@celery_app.task(name="app.tasks.guardian_tasks.ping_external_services")
def ping_external_services():
    """
    Ücretsiz bulut servislerinin uykuya dalmasını önlemek için periyodik olarak
    hepsine birer /health isteği atar.
    """
    logger.info("Platform Guardian: Harici servisleri aktif tutma görevi başlatıldı.")
    asyncio.run(ping_all_services())
    return "All external services have been pinged."