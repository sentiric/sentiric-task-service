# ⚙️ Sentiric Task Service

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-Celery_&_FastAPI-blueviolet.svg)](https://docs.celeryq.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Sentiric Task Service**, Sentiric platformunun asenkron "iş atıdır". Anlık yanıt gerektirmeyen, uzun süren veya periyodik olarak çalışması gereken tüm görevleri (örneğin: toplu rapor oluşturma, e-posta gönderme, veritabanı temizliği, AI modelinin yeniden eğitimi) arka planda güvenilir bir şekilde yönetir ve yürütür.

Bu servis, platformun ana diyalog akışını bloke etmeden ağır işlerin yapılabilmesini sağlayarak, sistemin genel performansını ve yanıt verme hızını korur.

## ✨ Temel Özellikler ve Mimari

*   **Güçlü Görev Kuyruğu:** Python ekosisteminin endüstri standardı olan **Celery**'yi temel alır.
*   **Dayanıklı Mesajlaşma:** Görevlerin güvenilir bir şekilde iletilmesi için **RabbitMQ**'yu mesaj broker'ı olarak kullanır.
*   **Sonuç Depolama:** Tamamlanan görevlerin sonuçlarını ve durumlarını saklamak için **Redis**'i backend olarak kullanır.
*   **Ayrık Ölçeklendirme:** Mimari, iki ana bileşenden oluşur:
    1.  **API Sunucusu (`task-service-api`):** FastAPI ile yazılmış, diğer servislerden yeni görev taleplerini alan ve anında bir `task_id` ile yanıt dönen arayüz.
    2.  **Worker (`task-service-worker`):** RabbitMQ'daki kuyruğu dinleyen ve asıl işi yapan, bağımsız olarak ölçeklendirilebilen arka plan işlemcisi.
*   **Canlı İzleme:** **Flower** entegrasyonu sayesinde, çalışan görevleri, işçilerin durumunu ve görev geçmişini `http://localhost:5555` adresinden canlı olarak izleme imkanı sunar.

## 🚀 Hızlı Başlangıç (Docker ile)

Bu servis, `sentiric-infrastructure` reposundaki merkezi `docker-compose` ile platformun bir parçası olarak çalışmak üzere tasarlanmıştır. Tek başına çalıştırmak ve test etmek için:

1.  **Altyapıyı Başlatın:** `task-service`, `rabbitmq` ve `redis` servislerine bağımlıdır. `sentiric-infrastructure` reposundan bu servisleri başlatın:
    ```bash
    docker compose up -d rabbitmq redis
    ```

2.  **`.env` Dosyası Oluşturun:**
    Proje için gerekli `RABBITMQ_URL` ve `REDIS_URL` gibi ortam değişkenlerini içeren bir `.env` dosyası oluşturun.

3.  **Servisi Başlatın:**
    ```bash
    # `docker-compose.service.yml` dosyasının bulunduğu dizinde
    docker compose -f docker-compose.service.yml up --build -d
    ```
    Loglarda `celery@... ready.` mesajını gördüğünüzde servis görevleri kabul etmeye hazırdır.

## 🤖 API Kullanımı ve Demo

Servisin API'ını test etmek ve uçtan uca bir görevin yaşam döngüsünü görmek için lütfen aşağıdaki rehberi inceleyin:

➡️ **[API Kullanım ve Demo Rehberi (DEMO.md)](DEMO.md)**

## 💻 Yerel Geliştirme ve Test

1.  Python 3.11+ ve `pip` kurulu olduğundan emin olun.
2.  Bir sanal ortam oluşturun ve aktif hale getirin.
3.  Projeyi "düzenlenebilir modda" ve geliştirme bağımlılıklarıyla birlikte kurun:
    ```bash
    pip install -e ".[dev]"
    ```
4.  Testleri çalıştırın:
    ```bash
    pytest -v
    ```

---
