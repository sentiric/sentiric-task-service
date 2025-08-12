# ⚙️ Sentiric Task Service

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Celery_&_FastAPI-blueviolet.svg)](https://docs.celeryq.dev/)

**Sentiric Task Service**, Sentiric platformunun asenkron "iş atıdır". Anlık yanıt gerektirmeyen, uzun süren veya periyodik olarak çalışması gereken tüm görevleri (örneğin: toplu rapor oluşturma, e-posta gönderme, veritabanı temizliği) arka planda güvenilir bir şekilde yönetir ve yürütür.

Bu servis, platformun ana diyalog akışını bloke etmeden ağır işlerin yapılabilmesini sağlayarak, sistemin genel performansını ve yanıt verme hızını korur.

## 🎯 Temel Sorumluluklar

*   **Asenkron Görev Yürütme:** Diğer servislerden gelen görev taleplerini alır ve bunları bir kuyruğa ekleyerek arka planda işler.
*   **Görev Durumu İzleme:** Her göreve benzersiz bir `task_id` atar ve bu ID üzerinden görevin durumunun (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`) sorgulanmasını sağlayan bir API sunar.
*   **İzleme Arayüzü:** **Flower** entegrasyonu sayesinde, çalışan görevleri, işçilerin durumunu ve görev geçmişini canlı olarak izleme imkanı sunar.
*   **Dayanıklılık:** Mesaj broker'ı (RabbitMQ) sayesinde, worker'lar veya API sunucusu çökse bile görevlerin kaybolmamasını sağlar.

## 🛠️ Teknoloji Yığını

*   **Dil:** Python
*   **Görev Kuyruğu:** Celery
*   **Mesaj Broker'ı:** RabbitMQ
*   **Sonuç Deposu:** Redis
*   **API Çerçevesi:** FastAPI
*   **İzleme:** Flower

## 🔌 API Etkileşimleri

*   **Gelen (Sunucu):**
    *   Herhangi bir iç servis (REST/JSON): `/api/v1/tasks/...` endpoint'lerine görev tetikleme istekleri alır.
*   **Giden (İstemci):**
    *   Bu servis, görevlerin doğasına bağlı olarak diğer servislere veya veritabanlarına istek atabilir.

## 🚀 Yerel Geliştirme

1.  **Platformu Başlatın:** Bu servis `rabbitmq` ve `redis`'e bağımlıdır. `sentiric-infrastructure`'dan `make up` komutuyla tüm platformu başlatın.
2.  **Bağımlılıkları Kurun:** `pip install -e ".[dev]"`
3.  **Servisi Başlatın:**
    *   Bir terminalde API sunucusunu başlatın: `uvicorn app.main:app --reload --port 5003`
    *   Başka bir terminalde Celery worker'ını başlatın: `celery -A app.core.celery_app worker -l info`
4.  **Testleri Çalıştırın:** `pytest -v`

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen projenin ana [Sentiric Governance](https://github.com/sentiric/sentiric-governance) reposundaki kodlama standartlarına ve katkıda bulunma rehberine göz atın.

---
## 🏛️ Anayasal Konum

Bu servis, [Sentiric Anayasası'nın (v11.0)](https://github.com/sentiric/sentiric-governance/blob/main/docs/blueprint/Architecture-Overview.md) **Zeka & Orkestrasyon Katmanı**'nda yer alan merkezi bir bileşendir.