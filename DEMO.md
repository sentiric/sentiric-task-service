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
API, görevi kabul ettiğini belirtmek için size anında bir `task_id` dönecektir.

```json
{"task_id":"<size_benzersiz_task_id>","status":"PENDING"}
```

### Adım 2: Görevin Durumunu İzleme

#### Yöntem A: Flower Web Arayüzü

1.  Tarayıcınızı açın ve `http://localhost:5555` adresine gidin.
2.  **"Tasks"** sekmesine tıklayın.
3.  Görevinizin durumunun **"Received"** -> **"Started"** -> **"Succeeded"** olarak değiştiğini canlı izleyebilirsiniz.

#### Yöntem B: Worker Logları

`make logs SERVICES="task-service-worker"` komutuyla worker loglarında görevin alındığını ve tamamlandığını görebilirsiniz.

### Adım 3: Görevin Sonucunu API'den Alma

Yaklaşık 5-6 saniye sonra, Adım 1'de aldığınız `task_id`'yi kullanarak API'den nihai sonucu sorgulayın.

```bash
# <size_benzersiz_task_id> kısmını kendi ID'nizle değiştirin
curl http://localhost:5003/api/v1/tasks/status/<size_benzersiz_task_id>
```

**Başarılı Yanıt:**
API, görevin durumunun "SUCCESS" olduğunu ve sonucunun `8` olduğunu teyit edecektir.

```json
{"task_id":"<size_benzersiz_task_id>","status":"SUCCESS","result":8}
```