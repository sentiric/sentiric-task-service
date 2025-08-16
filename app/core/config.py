from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from urllib.parse import urlparse
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    # Celery için zorunlu olanlar
    RABBITMQ_URL: str
    REDIS_URL: str

    # YENİ EKLENENLER: Platform Guardian görevinin ihtiyaç duyduğu değişkenler
    POSTGRES_URL: str
    VECTOR_DB_HOST: str   # <-- YENİ
    VECTOR_DB_PORT: int   # <-- YENİ
    # YENİ: Yeni boolean ayarımızı ekliyoruz.
    VECTOR_DB_USE_HTTPS: bool = False    
    VECTOR_DB_URL: str
    QDRANT_API_KEY: Optional[str] = Field(None)

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