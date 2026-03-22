import uuid
from fastapi import APIRouter, Cookie, Response
from typing import Optional
from itsdangerous import URLSafeSerializer, BadSignature
from models import LoginRequest
from db import USERS_DB

router = APIRouter(tags=["Задание 5.2 — Подписанные cookie (itsdangerous)"])

SECRET_KEY = "super-secret-key-for-kr2"
serializer = URLSafeSerializer(SECRET_KEY)

# Хранилище: {user_id (UUID str): username}
USER_SESSIONS: dict[str, str] = {}


def make_token(user_id: str) -> str:
    """Создаёт подписанный токен вида <user_id>.<signature>."""
    return serializer.dumps(user_id)


def verify_token(token: str) -> Optional[str]:
    """Проверяет подпись и возвращает user_id или None."""
    try:
        return serializer.loads(token)
    except BadSignature:
        return None


@router.post("/login52")
def login52(credentials: LoginRequest, response: Response):
    """
    Логин с подписанным cookie.
    Маршрут: POST /login52
    """
    user = USERS_DB.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        response.status_code = 401
        return {"message": "Invalid credentials"}

    user_id = str(uuid.uuid4())
    USER_SESSIONS[user_id] = credentials.username
    token = make_token(user_id)

    response.set_cookie(key="session_token", value=token, httponly=True, max_age=3600)
    return {"message": "Login successful", "session_token": token}


@router.get("/profile")
def get_profile(response: Response, session_token: Optional[str] = Cookie(default=None)):
    """
    Защищённый маршрут /profile.
    Проверяет подпись cookie, затем ищет пользователя по user_id.
    """
    if session_token is None:
        response.status_code = 401
        return {"message": "Unauthorized"}

    user_id = verify_token(session_token)
    if user_id is None or user_id not in USER_SESSIONS:
        response.status_code = 401
        return {"message": "Unauthorized"}

    username = USER_SESSIONS[user_id]
    user = USERS_DB[username]
    return {"user_id": user_id, "username": user["username"], "email": user["email"]}
