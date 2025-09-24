from pydantic import BaseModel
from uuid import UUID


class AddItemRequest(BaseModel):
    product_id: UUID
    quantity: int

class OrderItemResponse(BaseModel):
    product_id: UUID
    quantity: int
    order_id: UUID
