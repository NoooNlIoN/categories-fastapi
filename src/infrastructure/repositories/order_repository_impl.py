from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.models.order import Order
from src.domain.models.order_items import OrderItem
from src.domain.models.product import Product
from src.domain.repositories.order_repository import OrderRepository


class OrderNotFound(Exception):
    pass


class ProductNotFound(Exception):
    pass


class OutOfStock(Exception):
    pass


class InvalidQuantity(Exception):
    pass


@dataclass
class OrderItemResult:
    order_id: UUID
    product_id: UUID
    quantity: int


class OrderRepositoryImpl(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, order_id: UUID, *, with_items: bool = True) -> Optional[Order]:
        query = select(Order).where(Order.id == order_id)
        if with_items:
            query = query.options(
                selectinload(Order.items)
            )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def save(self, order: Order) -> None:
        self._session.add(order)

    async def add_item_to_order(
        self, order_id: UUID, product_id: UUID, quantity: int
    ) -> OrderItemResult:
        if quantity <= 0:
            raise InvalidQuantity("Quantity must be greater than zero")

        async with self._session.begin():
            order = await self.get_by_id(order_id, with_items=True)
            if order is None:
                raise OrderNotFound(str(order_id))

            product_query = (
                select(Product)
                .where(Product.id == product_id)
                .with_for_update()
            )
            product_result = await self._session.execute(product_query)
            product = product_result.scalar_one_or_none()
            if product is None:
                raise ProductNotFound(str(product_id))

            existing_item: Optional[OrderItem] = next(
                (item for item in (order.items or []) if item.product_id == product_id),
                None,
            )

            delta_to_add = quantity
            if delta_to_add > product.quantity:
                raise OutOfStock("Not enough product in stock")

            if existing_item is None:
                new_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    price=product.price,
                )
                if order.items is None:
                    order.items = []
                order.items.append(new_item)
                final_quantity = quantity
            else:
                existing_item.quantity += quantity
                final_quantity = existing_item.quantity

            product.quantity -= delta_to_add

            self._session.add(order)
            self._session.add(product)

        return OrderItemResult(
            order_id=order_id,
            product_id=product_id,
            quantity=final_quantity,
        )

