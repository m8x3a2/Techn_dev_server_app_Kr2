import uuid
import time
import hmac
import hashlib
from fastapi import APIRouter, Cookie, Response
from typing import Optional
from models import LoginRequest
from db import USERS_DB

router = APIRouter(tags=["Задание 5.3 — Динамическая сессия"])

SECRET_KEY = b"dynamic-session-secret-kr2"
SESSION_TTL = 300        # 5 минут (секунды)
RENEW_THRESHOLD = 180    # 3 минуты — порог продления


def _sign(data: str) -> str:
    return hmac.new(SECRET_KEY, data.encode(), hashlib.sha256).hexdigest()


def make_token53(user_id: str, timestamp: float) -> str:
    """Формирует токен: <user_id>.<timestamp>.<signature>"""
    payload = f"{user_id}.{int(timestamp)}"
    sig = _sign(payload)
    return f"{payload}.{sig}"


def parse_token53(token: str) -> Optional[tuple[str, int]]:
    """
    Разбирает и проверяет токен.
    Возвращает (user_id, timestamp) или None при ошибке.
    """
    try:
        parts = token.split(".")
        # UUID содержит 5 сегментов через '-', собираем его обратно
        # Формат: <uuid5parts>.<timestamp>.<signature>
        # uuid4 = 8-4-4-4-12 → при split(".") это 3 части uuid + timestamp + sig
        # Удобнее хранить UUID без дефисов или искать по индексу с конца
        sig_received = parts[-1]
        timestamp = parts[-2]
        user_id = ".".join(parts[:-2])
        payload = f"{user_id}.{timestamp}"
        expected_sig = _sign(payload)
        if not hmac.compare_digest(sig_received, expected_sig):
            return None
        return user_id, int(timestamp)
    except Exception:
        return None


# Хранилище: {user_id: username}
SESSIONS53: dict[str, str] = {}


@router.post("/login53")
def login53(credentials: LoginRequest, response: Response):
    user = USERS_DB.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        response.status_code = 401
        return {"message": "Invalid credentials"}

    user_id = str(uuid.uuid4())
    SESSIONS53[user_id] = credentials.username
    now = time.time()
    token = make_token53(user_id, now)

    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,   # False для тестирования; в проде — True
        max_age=SESSION_TTL,
    )
    return {"message": "Login successful", "session_token": token}


@router.get("/profile53")
def profile53(response: Response, session_token: Optional[str] = Cookie(default=None)):
    """
    Защищённый маршрут с динамическим TTL.
    - < 3 мин с последней активности  → кука не обновляется
    - 3–5 мин с последней активности  → кука обновляется на 5 мин
    - > 5 мин с последней активности  → 401 Session expired
    """
    if session_token is None:
        response.status_code = 401
        return {"message": "Unauthorized"}

    parsed = parse_token53(session_token)
    if parsed is None:
        response.status_code = 401
        return {"message": "Invalid session"}

    user_id, last_active = parsed
    now = time.time()
    elapsed = now - last_active

    if elapsed >= SESSION_TTL:
        response.status_code = 401
        return {"message": "Session expired"}

    if user_id not in SESSIONS53:
        response.status_code = 401
        return {"message": "Session expired"}

    username = SESSIONS53[user_id]
    user = USERS_DB[username]

    # Обновляем куку только если прошло >= 3 минуты (но < 5)
    if elapsed >= RENEW_THRESHOLD:
        new_token = make_token53(user_id, now)
        response.set_cookie(
            key="session_token",
            value=new_token,
            httponly=True,
            secure=False,
            max_age=SESSION_TTL,
        )

    return {
        "user_id": user_id,
        "username": user["username"],
        "email": user["email"],
        "session_age_seconds": round(elapsed, 1),
    }
