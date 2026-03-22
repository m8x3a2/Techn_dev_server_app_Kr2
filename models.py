from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re


# Задание 3.1
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    is_subscribed: Optional[bool] = None

    @field_validator("age")
    @classmethod
    def age_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError("age must be a positive integer")
        return v


# Задание 3.2
class Product(BaseModel):
    product_id: int
    name: str
    category: str
    price: float


# Задания 5.1 / 5.2 / 5.3
class LoginRequest(BaseModel):
    username: str
    password: str


# Задание 5.5
class CommonHeaders(BaseModel):
    user_agent: str
    accept_language: str

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, v):
        # Проверяем формат вида: en-US,en;q=0.9,es;q=0.8
        pattern = r'^[a-zA-Z\-\*]+(;q=\d(\.\d)?)?(,[a-zA-Z\-\*]+(;q=\d(\.\d)?)?)*$'
        if not re.match(pattern, v):
            raise ValueError("Accept-Language header has invalid format")
        return v

    model_config = {"populate_by_name": True}
