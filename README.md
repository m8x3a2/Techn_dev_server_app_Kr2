# КР №2 — Технологии разработки серверных приложений

## Установка и запуск

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Документация Swagger: http://127.0.0.1:8000/docs

---

## Структура проекта

```
kr2/
├── app.py            # Точка входа, подключение всех роутеров
├── models.py         # Pydantic-модели
├── db.py             # Симуляция базы данных
├── requirements.txt
└── routers/
    ├── task31.py     # Задание 3.1 — POST /create_user
    ├── task32.py     # Задание 3.2 — GET /product/{id}, GET /products/search
    ├── task51.py     # Задание 5.1 — Cookie-аутентификация (UUID)
    ├── task52.py     # Задание 5.2 — Подписанные cookie (itsdangerous)
    ├── task53.py     # Задание 5.3 — Динамический TTL сессии
    ├── task54.py     # Задание 5.4 — Заголовки User-Agent / Accept-Language
    └── task55.py     # Задание 5.5 — CommonHeaders модель (DRY)
```

---

## Описание заданий и примеры запросов

### Задание 3.1 — POST /create_user

Pydantic-модель `UserCreate` с валидацией полей.

```bash
curl -X POST http://localhost:8000/create_user \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com","age":30,"is_subscribed":true}'
```

---

### Задание 3.2 — GET /product/{product_id} и GET /products/search

> Маршрут `/products/search` объявлен **раньше** `/product/{product_id}`, чтобы FastAPI не пытался привести `"search"` к `int`.

```bash
# Получить продукт по ID
curl http://localhost:8000/product/123

# Поиск по ключевому слову
curl "http://localhost:8000/products/search?keyword=phone&category=Electronics&limit=5"
```

---

### Задание 5.1 — Cookie-аутентификация (простая)

```bash
# Логин — получаем cookie session_token
curl -c cookies.txt -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}'

# Доступ к профилю с cookie
curl -b cookies.txt http://localhost:8000/user

# Без cookie → 401
curl http://localhost:8000/user
```

---

### Задание 5.2 — Подписанные cookie (itsdangerous)

Токен имеет вид `<user_id>.<signature>`. Любое изменение cookie → 401.

```bash
curl -c c52.txt -X POST http://localhost:8000/login52 \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}'

curl -b c52.txt http://localhost:8000/profile
```

---

### Задание 5.3 — Динамический TTL сессии

Формат токена: `<user_id>.<timestamp>.<hmac_signature>`

| Прошло с последней активности | Действие |
|---|---|
| < 3 мин | Кука **не** обновляется |
| 3–5 мин | Кука **обновляется** на 5 мин |
| > 5 мин | **401 Session expired** |

```bash
curl -c c53.txt -X POST http://localhost:8000/login53 \
  -H "Content-Type: application/json" \
  -d '{"username":"user123","password":"password123"}'

curl -b c53.txt http://localhost:8000/profile53
```

---

### Задание 5.4 — Заголовки запроса

```bash
curl http://localhost:8000/headers \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  -H "Accept-Language: en-US,en;q=0.9,es;q=0.8"

# Без заголовков → 400
curl http://localhost:8000/headers
```

---

### Задание 5.5 — CommonHeaders (DRY)

Зависимость `extract_common_headers` переиспользуется в двух маршрутах.

```bash
curl http://localhost:8000/headers55 \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  -H "Accept-Language: en-US,en;q=0.9"

curl http://localhost:8000/info \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)" \
  -H "Accept-Language: en-US,en;q=0.9"
# Ответ содержит HTTP-заголовок X-Server-Time
```

---

## Тестовые пользователи

| username | password |
|---|---|
| user123 | password123 |
| admin | admin123 |
