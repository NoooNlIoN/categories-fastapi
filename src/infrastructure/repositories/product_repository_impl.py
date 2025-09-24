from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.product import Product
from src.domain.repositories.product_repository import ProductRepository


class ProductRepositoryImpl(ProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id_for_update(self, product_id: UUID) -> Optional[Product]:
        query = (
            select(Product)
            .where(Product.id == product_id)
            .with_for_update()
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def save(self, product: Product) -> None:
        self._session.add(product)

