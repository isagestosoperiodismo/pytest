from typing import List
from pydantic import BaseModel, Field


class Item(BaseModel):
    price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    items: List[Item]
    apply_discount: bool = False


class UserCreate(BaseModel):
    username: str
    email: str


class OrderResponse(BaseModel):
    id: int
    total: float
    discount_applied: bool
    items: List[Item]
    created_at: str
