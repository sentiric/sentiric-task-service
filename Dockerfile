FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY app ./app
COPY README.md .

RUN pip install .

# Bu Dockerfile hem API hem de Worker için kullanılacak.
# Hangi komutun çalışacağı docker-compose'da belirlenecek.
# Bu yüzden varsayılan bir CMD eklemiyoruz.