# ⚙️ Sentiric Task Service - Görev Listesi

Bu servisin mevcut ve gelecekteki tüm geliştirme görevleri, platformun merkezi görev yönetimi reposu olan **`sentiric-tasks`**'ta yönetilmektedir.

➡️ **[Aktif Görev Panosuna Git](https://github.com/sentiric/sentiric-tasks/blob/main/TASKS.md)**

---
Bu belge, servise özel, çok küçük ve acil görevler için geçici bir not defteri olarak kullanılabilir.

## Faz 1: Temel Asenkron Görev Yönetimi (INFRA-02)
- [x] Celery Broker (RabbitMQ) ve Backend (Redis) ile uygulama başlatıldı.
- [x] FastAPI API (Task Dispatch ve Status Query) hazırlandı.
- [x] Örnek görev (`long_running_task`) ve periyodik görev (`ping_external_services`) tanımlandı.
- [ ] Flower için konfigürasyon eklenecek (docker-compose.tools.yml içinde). (CONTROL-TASK-01)