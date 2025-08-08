from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import urlparse

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    # YENİ: Loglama için gerekli ayarlar
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    # .env dosyasındaki değişkenlerle eşleşen alanlar
    RABBITMQ_URL: str
    REDIS_URL: str

    # Celery bu isimleri bekliyor, bu yüzden property olarak tanımlıyoruz
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        parsed_url = urlparse(self.REDIS_URL)
        if not parsed_url.path or parsed_url.path == '/':
            return f"{self.REDIS_URL.rstrip('/')}/0"
        return self.REDIS_URL

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()