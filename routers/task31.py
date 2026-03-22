from fastapi import APIRouter
from models import UserCreate

router = APIRouter(tags=["Задание 3.1 — Создание пользователя"])


@router.post("/create_user")
def create_user(user: UserCreate):
    """
    Принимает данные пользователя и возвращает их обратно.
    Поля: name (обяз.), email (обяз., валидный), age (необяз., > 0), is_subscribed (необяз., bool).
    """
    return user
