## Локальный запуск

### Todo

```bash
cd todo_app
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### ShortURL

```bash
cd shorturl_app
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

---

## Docker

### Создать volumes

```bash
docker volume create todo_data
docker volume create shorturl_data
```

### Собрать образы

```bash
docker build -t todo-service ./todo_app
docker build -t shorturl-service ./shorturl_app
```

### Запустить контейнеры

```bash
# Todo
docker run -d -p 8000:80 -v todo_data:/app/data --name todo_service todo-service

# ShortURL
docker run -d -p 8001:80 -v shorturl_data:/app/data --name shorturl_service shorturl-service
```

---
