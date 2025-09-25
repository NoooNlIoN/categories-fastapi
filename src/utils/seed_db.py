import asyncio
from decimal import Decimal

from src.infrastructure.database.engine import AsyncSessionLocal
from src.domain.models.category import Category
from src.domain.models.client import Client
from src.domain.models.product import Product
from src.domain.models.order import Order
from src.domain.models.order_items import OrderItem


async def create_test_data():
    async with AsyncSessionLocal() as session:
        try:
            category = Category(
                name="Электроника"
            )
            session.add(category)
            await session.flush()
            
            client = Client(
                name="Иван Петров",
                address="г. Москва, ул. Тестовая, д. 1"
            )
            session.add(client)
            await session.flush()
            
            product = Product(
                name="iPhone 15",
                quantity=10,
                price=Decimal("99999.99"),
                category_id=category.id
            )
            session.add(product)
            await session.flush()
            
            order = Order(
                client_id=client.id
            )
            session.add(order)
            await session.flush()
            
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=2,
                price=product.price
            )
            session.add(order_item)
            await session.flush()
            
            await session.commit()
            print("Выполнено успешно")
            
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            await session.rollback()
            raise


async def main():
    try:
        await create_test_data()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))
