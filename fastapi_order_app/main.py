
from fastapi import FastAPI, HTTPException, status
from typing import List
from sqlmodel import SQLModel, Session, select
import models, schemas
from database import engine, init_db
import crud

app = FastAPI(title="Orders API")

@app.on_event('startup')
def on_startup():
    init_db()

# Customer endpoints
@app.post('/customers/', response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(payload: schemas.CustomerCreate):
    customer = models.Customer(**payload.dict())
    customer = crud.create_customer(customer)
    return customer

@app.get('/customers/{customer_id}/total_spend')
def customer_total_spend(customer_id: int):
    cust = crud.get_customer(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail='Customer not found')
    total = crud.customer_total_spend(customer_id)
    return {'customer_id': customer_id, 'total_spend': total}

# Create order with nested items
@app.post('/orders/', response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: schemas.OrderCreate):
    # Validate customer exists
    from crud import get_customer
    if not get_customer(payload.customer_id):
        raise HTTPException(status_code=404, detail='Customer not found')

    order = models.Order(customer_id=payload.customer_id, status=payload.status)
    if payload.date:
        order.date = payload.date

    items = [models.OrderItem(product_name=i.product_name, quantity=i.quantity, price=i.price) for i in payload.items]
    order = crud.create_order_with_items(order, items)

    # Reload order with items for response
    with Session(engine) as session:
        stmt = select(models.Order).where(models.Order.id == order.id)
        ord_db = session.exec(stmt).one()
        ord_db.items
        return ord_db

# Update order status with allowed transitions
@app.patch('/orders/{order_id}/status')
def update_order_status(order_id: int, status: models.OrderStatus):
    ord = crud.get_order(order_id)
    if not ord:
        raise HTTPException(status_code=404, detail='Order not found')
    allowed = {
        models.OrderStatus.DRAFT: [models.OrderStatus.CONFIRMED],
        models.OrderStatus.CONFIRMED: [models.OrderStatus.SHIPPED],
        models.OrderStatus.SHIPPED: []
    }
    if status == ord.status:
        return {'order_id': order_id, 'status': ord.status}
    if status not in allowed[ord.status]:
        raise HTTPException(status_code=400, detail=f'Invalid status transition from {ord.status} to {status}')
    ord.status = status
    ord = crud.update_order(ord)
    return {'order_id': order_id, 'status': ord.status}

# Delete order with prevention if shipped
@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int):
    ord = crud.get_order(order_id)
    if not ord:
        raise HTTPException(status_code=404, detail='Order not found')
    if ord.status == models.OrderStatus.SHIPPED:
        raise HTTPException(status_code=400, detail='Cannot delete an order that is already Shipped')
    crud.delete_order(ord)
    return None

# Simple endpoints to read orders and items
@app.get('/orders/{order_id}', response_model=schemas.OrderRead)
def read_order(order_id: int):
    ord = crud.get_order(order_id)
    if not ord:
        raise HTTPException(status_code=404, detail='Order not found')
    # ensure items loaded
    with Session(engine) as session:
        stmt = select(models.Order).where(models.Order.id == order_id)
        ord_db = session.exec(stmt).one()
        ord_db.items
        return ord_db

@app.get('/customers/{customer_id}', response_model=schemas.CustomerRead)
def read_customer(customer_id: int):
    cust = crud.get_customer(customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail='Customer not found')
    return cust
