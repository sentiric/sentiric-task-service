# ⚙️ Sentiric Task Service - Görev Listesi

Bu belge, `task-service`'in geliştirme yol haritasını ve önceliklerini tanımlar.

---

### Faz 1: Temel Asenkron Görev Yönetimi (Mevcut Durum)

Bu faz, servisin temel görev kabul etme, yürütme ve raporlama yeteneklerini oluşturmayı hedefler.

-   [x] **Celery Kurulumu:** RabbitMQ (broker) ve Redis (backend) ile çalışan Celery uygulaması.
-   [x] **FastAPI Arayüzü:** Görevleri tetiklemek (`POST /tasks/...`) ve durumlarını sorgulamak (`GET /tasks/status/{id}`) için API endpoint'leri.
-   [x] **Örnek Görev:** Mimarinin çalıştığını gösteren basit bir `long_running_task`.
-   [x] **Flower Entegrasyonu:** Görevleri ve worker'ları izlemek için canlı bir dashboard.
-   [x] **Dayanıklı Kurulum:** Servislerin `healthcheck`'ler ile birbirini beklemesini sağlayan `docker-compose` yapılandırması.

---

### Faz 2: Gerçek İş Görevleri ve Gelişmiş Özellikler (Sıradaki Öncelik)

Bu faz, servisi platformun gerçek ihtiyaçlarını karşılayan görevlerle donatmayı hedefler.

-   [ ] **Görev ID: TASK-001 - CDR Raporu Oluşturma Görevi**
    -   **Açıklama:** Belirtilen bir tarih aralığı ve `tenant_id` için `cdr-service`'in veritabanından veri çekip bir CSV/PDF raporu oluşturan ve sonucunda bir indirme linki dönen bir görev oluştur.
    -   **Durum:** ⬜ Planlandı.

-   [ ] **Görev ID: TASK-002 - Periyodik (Zamanlanmış) Görevler**
    -   **Açıklama:** `Celery Beat`'i entegre ederek, her gece yarısı eski logları temizleyen veya her sabah bir özet raporu e-postası gönderen gibi zamanlanmış görevler oluştur.
    -   **Durum:** ⬜ Planlandı.

-   [ ] **Görev ID: TASK-003 - Gelişmiş Hata Yönetimi ve Yeniden Deneme**
    -   **Açıklama:** Harici bir API'ye bağlanan bir görev başarısız olduğunda, görevin otomatik olarak (exponential backoff ile) birkaç kez daha denenmesini sağlayan politikaları implemente et.
    -   **Durum:** ⬜ Planlandı.