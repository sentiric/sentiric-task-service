from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from urllib.parse import urlparse
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    # Temel bağlantı bilgileri
    RABBITMQ_URL: str
    REDIS_URL: str
    POSTGRES_URL: str
    VECTOR_DB_HOST: str
    VECTOR_DB_PORT: int
    VECTOR_DB_URL: str # Bu artık sadece Qdrant istemcisi için kullanılmıyor, genel bir bilgi.
    QDRANT_API_KEY: Optional[str] = Field(None)
    
    # Ortama özel bayraklar
    VECTOR_DB_USE_HTTPS: bool = False
    REDIS_USE_SSL: bool = False # <-- YENİ AYAR

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        # Bu kısım doğru, Redis DB numarasını ekliyor.
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