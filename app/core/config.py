from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, Dict, Any
import ssl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    RABBITMQ_URL: str
    REDIS_URL: str
    
    LLM_SERVICE_URL: str
    STT_SERVICE_URL: str
    TTS_EDGE_SERVICE_URL: str
    KNOWLEDGE_SERVICE_URL: str
    
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL

    # YENİ: SSL/TLS ayarlarını yönetecek property'ler
    @property
    def CELERY_BROKER_OPTIONS(self) -> Dict[str, Any]:
        if self.RABBITMQ_URL.startswith("amqps"):
            return {
                "ssl_cert_reqs": ssl.CERT_NONE,
            }
        return {}
        
    @property
    def CELERY_REDIS_BACKEND_OPTIONS(self) -> Dict[str, Any]:
        if self.REDIS_URL.startswith("rediss"):
            return {
                "ssl_cert_reqs": ssl.CERT_NONE,
            }
        return {}

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()