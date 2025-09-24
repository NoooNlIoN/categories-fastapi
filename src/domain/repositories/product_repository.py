from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.product import Product


class ProductRepository(ABC):

    @abstractmethod
    async def get_by_id_for_update(self, product_id: UUID) -> Product | None:
        ...

    @abstractmethod
    async def save(self, product: Product) -> None:
        ...


