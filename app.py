from fastapi import FastAPI
from routers import task31, task32, task51, task52, task53, task54, task55

app = FastAPI(
    title="КР №2 — Технологии разработки серверных приложений",
    description=(
        "**Задание 3.1** — POST /create_user\n\n"
        "**Задание 3.2** — GET /products/search, GET /product/{product_id}\n\n"
        "**Задание 5.1** — POST /login, GET /user (cookie-аутентификация)\n\n"
        "**Задание 5.2** — POST /login52, GET /profile (подписанные cookie)\n\n"
        "**Задание 5.3** — POST /login53, GET /profile53 (динамический TTL)\n\n"
        "**Задание 5.4** — GET /headers\n\n"
        "**Задание 5.5** — GET /headers55, GET /info (CommonHeaders DRY)"
    ),
    version="1.0.0",
)

app.include_router(task31.router)
app.include_router(task32.router)
app.include_router(task51.router)
app.include_router(task52.router)
app.include_router(task53.router)
app.include_router(task54.router)
app.include_router(task55.router)


@app.get("/", tags=["Root"])
def root():
    return {"message": "КР №2 запущена. Документация: /docs"}
