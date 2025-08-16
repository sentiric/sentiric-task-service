from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from urllib.parse import urlparse
from typing import Optional
import ssl # SSL modülünü import ediyoruz

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    RABBITMQ_URL: str
    REDIS_URL: str
    POSTGRES_URL: str
    VECTOR_DB_HOST: str
    VECTOR_DB_PORT: int
    VECTOR_DB_URL: str
    QDRANT_API_KEY: Optional[str] = Field(None)
    
    VECTOR_DB_USE_HTTPS: bool = False
    REDIS_USE_SSL: bool = False

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        # DÜZELTME: REDIS_USE_SSL bayrağına göre URL'yi dinamik olarak zenginleştiriyoruz.
        base_url = self.REDIS_URL
        
        return base_url

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()