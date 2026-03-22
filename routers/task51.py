import uuid
from fastapi import APIRouter, Cookie, Response
from typing import Optional
from models import LoginRequest
from db import USERS_DB

router = APIRouter(tags=["Задание 5.1 — Cookie-аутентификация"])

# Хранилище активных сессий: {session_token: username}
SESSIONS: dict[str, str] = {}


@router.post("/login")
def login(credentials: LoginRequest, response: Response):
    """
    Принимает username и password.
    При успехе устанавливает httponly-cookie 'session_token' с UUID-значением.
    """
    user = USERS_DB.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        response.status_code = 401
        return {"message": "Invalid credentials"}

    token = str(uuid.uuid4())
    SESSIONS[token] = credentials.username
    response.set_cookie(key="session_token", value=token, httponly=True, max_age=3600)
    return {"message": "Login successful", "session_token": token}


@router.get("/user")
def get_user(response: Response, session_token: Optional[str] = Cookie(default=None)):
    """
    Защищённый маршрут. Требует валидный cookie 'session_token'.
    Возвращает профиль пользователя или 401.
    """
    if session_token is None or session_token not in SESSIONS:
        response.status_code = 401
        return {"message": "Unauthorized"}

    username = SESSIONS[session_token]
    user = USERS_DB[username]
    return {"username": user["username"], "email": user["email"]}
