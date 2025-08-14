# --- STAGE 1: Builder ---
FROM python:3.11-slim-bullseye AS builder

WORKDIR /app

ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    PIP_NO_CACHE_DIR=1
    
# Gerekli sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Proje tanımını kopyala
COPY pyproject.toml .

# Uygulama kodunu kopyala
COPY app ./app
COPY README.md .

# Bağımlılıklar dahil projeyi kur
RUN pip install .

# --- STAGE 2: Production ---
FROM python:3.11-slim-bullseye

WORKDIR /app

# Çalışma zamanı için gerekli paketler
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Root olmayan kullanıcı oluştur
RUN useradd -m -u 1001 sentiric_user

# Builder'dan sadece kurulu Python kütüphanelerini ve komutları kopyala
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Uygulama kodunu kopyala
COPY ./app ./app

# Dosya sahipliğini yeni kullanıcıya ver
RUN chown -R sentiric_user:sentiric_user /app

# Kullanıcıyı değiştir
USER sentiric_user

# FastAPI sunucusu için portu aç
EXPOSE 5003

# Varsayılan komut API sunucusunu başlatmak olsun.
# Worker için `docker-compose.dev.yml`'de 'command' ile override edeceğiz.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5003"]