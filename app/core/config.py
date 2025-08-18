from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Dict, Any
import ssl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    # Bu değişkenler doğrudan .env dosyasından okunacak
    RABBITMQ_URL: str
    REDIS_URL: str
    
    LLM_SERVICE_URL: str
    STT_SERVICE_URL: str
    TTS_EDGE_SERVICE_URL: str
    KNOWLEDGE_SERVICE_URL: str
    
    @property
    def CELERY_BROKER_URL(self) -> str:
        # Eğer URL "amqps" ile başlıyorsa, sonuna SSL seçeneğini ekle
        if self.RABBITMQ_URL.startswith("amqps"):
            # URL'de zaten query parametresi var mı kontrol et
            separator = "&" if "?" in self.RABBITMQ_URL else "?"
            return f"{self.RABBITMQ_URL}{separator}ssl_cert_reqs=CERT_NONE"
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        # Eğer URL "rediss" ile başlıyorsa, sonuna SSL seçeneğini ekle
        if self.REDIS_URL.startswith("rediss"):
            separator = "&" if "?" in self.REDIS_URL else "?"
            return f"{self.REDIS_URL}{separator}ssl_cert_reqs=CERT_NONE"
        return self.REDIS_URL

    # Bu property'ler artık gerekli değil ama silmek sorun yaratmaz
    @property
    def CELERY_BROKER_OPTIONS(self) -> Dict[str, Any]:
        return {}
        
    @property
    def CELERY_REDIS_BACKEND_OPTIONS(self) -> Dict[str, Any]:
        return {}

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()