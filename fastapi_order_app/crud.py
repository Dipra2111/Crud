
from sqlmodel import Session, select
from database import engine
import models
from typing import List

def create_customer(customer: models.Customer) -> models.Customer:
    with Session(engine) as session:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

def get_customer(customer_id: int):
    with Session(engine) as session:
        return session.get(models.Customer, customer_id)

def create_order_with_items(order: models.Order, items: List[models.OrderItem]) -> models.Order:
    with Session(engine) as session:
        session.add(order)
        session.commit()
        # ensure order.id is available
        session.refresh(order)
        for item in items:
            item.order_id = order.id
            session.add(item)
        session.commit()
        session.refresh(order)
        return order

def get_order(order_id: int):
    with Session(engine) as session:
        return session.get(models.Order, order_id)

def update_order(order: models.Order):
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

def delete_order(order: models.Order):
    with Session(engine) as session:
        session.delete(order)
        session.commit()

def customer_total_spend(customer_id: int) -> float:
    with Session(engine) as session:
        stmt = select(models.OrderItem).join(models.Order).where(models.Order.customer_id == customer_id)
        items = session.exec(stmt).all()
        # Consider only Confirmed and Shipped orders for total spend
        total = 0.0
        for it in items:
            order = session.get(models.Order, it.order_id)
            if order.status in (models.OrderStatus.CONFIRMED, models.OrderStatus.SHIPPED):
                total += it.quantity * it.price
        return total
