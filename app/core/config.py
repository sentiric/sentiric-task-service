# sentiric-task-service/app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, Dict, Any

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"
    SERVICE_VERSION: str = "0.1.0"

    # Celery Broker ve Backend Ayarları
    RABBITMQ_URL: str
    REDIS_URL: str
    
    # Platform Guardian için dış servis URL'leri
    LLM_SERVICE_URL: str = "http://llm-service:16010"
    STT_SERVICE_URL: str = "http://stt-service:15010"
    TTS_EDGE_SERVICE_URL: str = "http://tts-edge-service:14020"
    KNOWLEDGE_SERVICE_URL: str = "http://knowledge-service:12040"
    
    @property
    def CELERY_BROKER_URL(self) -> str:
        # Celery için RabbitMQ URL'si
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        # Celery sonuçları için Redis URL'si
        return f"{self.REDIS_URL}/0" # Redis'in 0 numaralı DB'sini kullan

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()