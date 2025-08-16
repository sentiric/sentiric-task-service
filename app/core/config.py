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
        
        # Eğer SSL kullanılıyorsa ve URL'de zaten parametre yoksa, ekle.
        if self.REDIS_USE_SSL and "ssl_cert_reqs" not in base_url:
            separator = "&" if "?" in base_url else "?"
            base_url += f"{separator}ssl_cert_reqs={ssl.CERT_NONE}"

        # Veritabanı numarasını ekle (eğer yoksa)
        parsed_url = urlparse(base_url)
        if not parsed_url.path or parsed_url.path == '/':
            return f"{base_url.rstrip('/')}/0"
        return base_url

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()