
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, conint, confloat
from models import OrderStatus

class OrderItemCreate(BaseModel):
    product_name: str
    quantity: conint(gt=0) = 1
    price: confloat(gt=0)

class OrderCreate(BaseModel):
    customer_id: int
    date: Optional[datetime] = None
    status: Optional[OrderStatus] = OrderStatus.DRAFT
    items: List[OrderItemCreate]

class OrderItemRead(BaseModel):
    id: int
    order_id: int
    product_name: str
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    id: int
    customer_id: int
    date: datetime
    status: OrderStatus
    items: List[OrderItemRead] = []

    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    name: str
    email: str

class CustomerRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
