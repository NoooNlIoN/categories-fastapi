from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.schemas.orders_schemas import AddItemRequest, OrderItemResponse
from src.infrastructure.database.engine import get_db
from src.infrastructure.repositories.order_repository_impl import (
    OrderRepositoryImpl,
    OrderNotFound,
    ProductNotFound,
    OutOfStock,
    InvalidQuantity,
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/{order_id}/items", response_model=OrderItemResponse)
async def add_item_to_order(
    order_id: UUID,
    request: AddItemRequest,
    db: AsyncSession = Depends(get_db),
) -> OrderItemResponse:
    order_repo = OrderRepositoryImpl(db)
    
    try:
        result = await order_repo.add_item_to_order(
            order_id=order_id,
            product_id=request.product_id,
            quantity=request.quantity,
        )
        
        return OrderItemResponse(
            order_id=result.order_id,
            product_id=result.product_id,
            quantity=result.quantity,
        )
    
    except OrderNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    except ProductNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    except OutOfStock:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Not enough product in stock",
        )
    except InvalidQuantity:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quantity must be greater than zero",
        )