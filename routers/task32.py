from fastapi import APIRouter, HTTPException
from typing import Optional
from db import SAMPLE_PRODUCTS

router = APIRouter(tags=["Задание 3.2 — Продукты"])


# ВАЖНО: /products/search должен быть объявлен РАНЬШЕ /product/{product_id},
# иначе FastAPI попытается привести "search" к int и выдаст ошибку.

@router.get("/products/search")
def search_products(
    keyword: str,
    category: Optional[str] = None,
    limit: int = 10,
):
    """
    Поиск товаров по ключевому слову и (опционально) категории.
    limit — максимальное количество результатов (по умолчанию 10).
    """
    results = [
        p for p in SAMPLE_PRODUCTS
        if keyword.lower() in p["name"].lower()
        and (category is None or p["category"].lower() == category.lower())
    ]
    return results[:limit]


@router.get("/product/{product_id}")
def get_product(product_id: int):
    """Возвращает информацию о продукте по его идентификатору."""
    for product in SAMPLE_PRODUCTS:
        if product["product_id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
