
from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class OrderStatus(str, Enum):
    DRAFT = "Draft"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str

    orders: List["Order"] = Relationship(back_populates="customer")

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customer.id")
    date: datetime = Field(default_factory=datetime.utcnow)
    status: OrderStatus = Field(default=OrderStatus.DRAFT)

    customer: Optional[Customer] = Relationship(back_populates="orders")
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_name: str
    quantity: int
    price: float

    order: Optional[Order] = Relationship(back_populates="items")
