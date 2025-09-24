from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.order import Order


class OrderRepository(ABC):

    @abstractmethod
    async def get_by_id(self, order_id: UUID, *, with_items: bool = True) -> Order | None:
        ...

    @abstractmethod
    async def save(self, order: Order) -> None:
        ...


