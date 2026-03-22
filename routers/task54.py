from fastapi import APIRouter, Header, HTTPException
from typing import Optional
import re

router = APIRouter(tags=["Задание 5.4 — Заголовки запросов"])

ACCEPT_LANG_PATTERN = re.compile(
    r'^[a-zA-Z\-\*]+(;q=\d(\.\d)?)?(,[a-zA-Z\-\*]+(;q=\d(\.\d)?)?)*$'
)


@router.get("/headers")
def get_headers(
    user_agent: Optional[str] = Header(default=None),
    accept_language: Optional[str] = Header(default=None),
):
    """
    GET /headers
    Извлекает заголовки User-Agent и Accept-Language.
    Возвращает 400, если один из них отсутствует или Accept-Language невалиден.
    """
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing required header: User-Agent")
    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing required header: Accept-Language")
    if not ACCEPT_LANG_PATTERN.match(accept_language):
        raise HTTPException(status_code=400, detail="Invalid Accept-Language header format")

    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language,
    }
