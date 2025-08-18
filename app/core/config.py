from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    ENV: str = "production"
    LOG_LEVEL: str = "INFO"

    RABBITMQ_URL: str
    REDIS_URL: str
    
    # --- YENİ EKLENEN ALANLAR ---
    # Guardian görevinin ping'leyeceği servislerin URL'leri
    LLM_SERVICE_URL: str
    STT_SERVICE_URL: str
    TTS_EDGE_SERVICE_URL: str
    KNOWLEDGE_SERVICE_URL: str
    # --- BİTTİ ---

    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return self.REDIS_URL

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()