FROM python:3.11-slim-bullseye

WORKDIR /app

ENV PIP_BREAK_SYSTEM_PACKAGES=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# YENİ: Root olmayan bir kullanıcı oluştur
RUN useradd -m -u 1001 sentiric_user

COPY pyproject.toml .
COPY app ./app
COPY README.md .

RUN pip install .

# YENİ: Dosya sahipliğini yeni kullanıcıya ver
RUN chown -R sentiric_user:sentiric_user /app

# YENİ: Kullanıcıyı değiştir
USER sentiric_user

# ...