from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from fastapi import Header
import re

router = APIRouter(tags=["Задание 5.5 — CommonHeaders модель (DRY)"])

ACCEPT_LANG_PATTERN = re.compile(
    r'^[a-zA-Z\-\*]+(;q=\d(\.\d)?)?(,[a-zA-Z\-\*]+(;q=\d(\.\d)?)?)*$'
)


def extract_common_headers(
    user_agent: Annotated[str | None, Header()] = None,
    accept_language: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Зависимость, которая извлекает и валидирует общие заголовки.
    Используется в обоих маршрутах (принцип DRY).
    """
    if not user_agent:
        raise HTTPException(status_code=400, detail="Missing required header: User-Agent")
    if not accept_language:
        raise HTTPException(status_code=400, detail="Missing required header: Accept-Language")
    if not ACCEPT_LANG_PATTERN.match(accept_language):
        raise HTTPException(status_code=400, detail="Invalid Accept-Language header format")
    return {"User-Agent": user_agent, "Accept-Language": accept_language}


from fastapi import Depends


@router.get("/headers55")
def headers55(headers: dict = Depends(extract_common_headers)):
    """
    GET /headers55
    Возвращает User-Agent и Accept-Language из модели CommonHeaders.
    (Маршрут переименован в /headers55, чтобы не конфликтовать с задание 5.4.)
    """
    return headers


@router.get("/info")
def info(headers: dict = Depends(extract_common_headers)):
    """
    GET /info
    Возвращает заголовки + приветственное сообщение.
    В ответе также присутствует HTTP-заголовок X-Server-Time.
    """
    body = {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": headers,
    }
    server_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    return JSONResponse(content=body, headers={"X-Server-Time": server_time})
