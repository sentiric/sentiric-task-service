### 📄 File: `README.md` | 🏷️ Markdown

```markdown
# ⚙️ Sentiric Task Service

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Language](https://img.shields.io/badge/language-Python-blue.svg)]()
[![Framework](https://img.shields.io/badge/framework-Celery_&_FastAPI-blueviolet.svg)]()

**Sentiric Task Service**, Sentiric platformunun asenkron "iş atıdır". Anlık yanıt gerektirmeyen, uzun süren veya periyodik olarak çalışması gereken tüm görevleri (örneğin: toplu rapor oluşturma, e-posta gönderme, veritabanı temizliği) arka planda güvenilir bir şekilde yönetir ve yürütür.

Bu servis, platformun ana diyalog akışını bloke etmeden ağır işlerin yapılabilmesini sağlayarak, sistemin genel performansını ve yanıt verme hızını korur.

## 🎯 Temel Sorumluluklar

*   **Asenkron Görev Yürütme:** Görev taleplerini alır ve kuyruğa ekleyerek arka planda işler.
*   **Görev Durumu İzleme:** Görev durumunun (`PENDING`, `STARTED`, `SUCCESS`, `FAILURE`) sorgulanmasını sağlayan bir API sunar.
*   **Periyodik Görevler:** Celery Beat ile zamanlanmış görevleri yönetir.
*   **Dayanıklılık:** Mesaj broker'ı (RabbitMQ) sayesinde görevlerin kaybolmamasını sağlar.

## 🛠️ Teknoloji Yığını

*   **Dil:** Python 3.11
*   **Görev Kuyruğu:** Celery
*   **Mesaj Broker'ı:** RabbitMQ
*   **Sonuç Deposu:** Redis
*   **API Çerçevesi:** FastAPI
*   **İzleme:** Prometheus, Flower (Harici araç)

## 🔌 API Etkileşimleri

*   **Gelen (Sunucu):**
    *   İç servisler (REST/JSON): `/api/v1/tasks/...` endpoint'lerine görev tetikleme istekleri alır.
*   **Giden (İstemci):**
    *   Diğer servislere (/health pingleri, data senkronizasyonu).

---
## 🏛️ Anayasal Konum

Bu servis, [Sentiric Anayasası'nın](https://github.com/sentiric/sentiric-governance) **Horizontal Capability Layer**'ında yer alan merkezi bir bileşendir.