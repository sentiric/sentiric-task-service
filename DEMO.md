# ⚙️ Sentiric Task Service - API Kullanım ve Demo Rehberi

Bu belge, çalışan `sentiric-task-service`'in yeteneklerini uçtan uca nasıl test edeceğinizi gösterir.

## Önkoşullar

*   `docker compose` ile tüm servislerin (`task-service`, `task-service-worker`, `flower`) çalışır durumda olması.
*   `curl` veya benzeri bir HTTP istemcisinin terminalinizde kurulu olması.

---

## Uçtan Uca Test Senaryosu

Bu senaryoda, 5 saniye süren basit bir toplama görevini tetikleyeceğiz, durumunu izleyeceğiz ve sonucunu alacağız.

### Adım 1: Görevi Tetikleme

Aşağıdaki komut, `5 + 3` işlemini yapacak olan `long_running_task` görevini arka planda çalışması için Celery kuyruğuna gönderir.

```bash
curl -X POST "http://localhost:5003/api/v1/tasks/long_task" \
-H "Content-Type: application/json" \
-d '{"x": 5, "y": 3}'
```

**Başarılı Yanıt:**
API, görevi kabul ettiğini ve arka planda çalışmaya başladığını belirtmek için size anında bir `task_id` dönecektir. Bu ID, görevinizi takip etmek için anahtarınızdır.

```json
{"task_id":"<size_benzersiz_task_id>","status":"PENDING"}
```

### Adım 2: Görevin Durumunu İzleme (İki Yöntem)

#### Yöntem A: Flower Web Arayüzü

1.  Tarayıcınızı açın ve `http://localhost:5555` adresine gidin.
2.  **"Tasks"** sekmesine tıklayın.
3.  Az önce oluşturduğunuz görevi listede göreceksiniz. Durumunun önce **"Received"**, sonra **"Started"** ve 5 saniye sonra **"Succeeded"** olarak değiştiğini canlı olarak izleyebilirsiniz.

![Flower Arayüzü](https://docs.celeryq.dev/en/stable/_images/flower-tasks.png)

#### Yöntem B: Worker Logları

`docker compose -f docker-compose.service.yml logs -f task-service-worker` komutunu çalıştırdığınız terminalde aşağıdaki gibi loglar göreceksiniz:

```
# 1. Görevin alındığı an
[INFO/MainProcess] Task app.tasks.example_tasks.long_running_task[...] received

# 2. Görevin başarıyla tamamlandığı an (5 saniye sonra)
[INFO/ForkPoolWorker-2] Task app.tasks.example_tasks.long_running_task[...] succeeded in 5.004s: 8
```

### Adım 3: Görevin Sonucunu API'den Alma

Görevin tamamlandığından emin olduktan sonra (yaklaşık 5-6 saniye sonra), Adım 1'de aldığınız `task_id`'yi kullanarak API'den nihai sonucu sorgulayabilirsiniz.

```bash
# <size_benzersiz_task_id> kısmını kendi ID'nizle değiştirin
curl http://localhost:5003/api/v1/tasks/status/<size_benzersiz_task_id>
```

**Başarılı Yanıt:**
API, görevin durumunun "SUCCESS" olduğunu ve sonucunun `8` olduğunu teyit edecektir.

```json
{"task_id":"<size_benzersiz_task_id>","status":"SUCCESS","result":8}
```

Bu üç adımlı süreç, `sentiric-task-service`'in asenkron görevleri başarıyla kabul ettiğini, yürüttüğünü ve sonuçlarını güvenilir bir şekilde sunduğunu kanıtlar.
