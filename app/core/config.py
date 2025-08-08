from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import urlparse

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sentiric Task Service"
    API_V1_STR: str = "/api/v1"
    
    # .env dosyasındaki değişkenlerle eşleşen alanlar
    RABBITMQ_URL: str
    REDIS_URL: str

    # Celery bu isimleri bekliyor, bu yüzden property olarak tanımlıyoruz
    @property
    def CELERY_BROKER_URL(self) -> str:
        return self.RABBITMQ_URL

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        # --- YENİ VE DAHA SAĞLAM MANTIK ---
        # 1. Gelen REDIS_URL'sini ayrıştır.
        parsed_url = urlparse(self.REDIS_URL)
        
        # 2. Eğer URL'nin path'i (yani /db_numarası kısmı) boşsa veya sadece '/' ise,
        #    o zaman sonuna '/0' ekle.
        if not parsed_url.path or parsed_url.path == '/':
            return f"{self.REDIS_URL.rstrip('/')}/0"
            
        # 3. Eğer zaten bir veritabanı numarası belirtilmişse, URL'yi olduğu gibi kullan.
        return self.REDIS_URL

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()