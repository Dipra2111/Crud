FastAPI Order Management App
Overview
Simple FastAPI application with SQLite and SQLModel implementing:

Customer (id, name, email)
Order (id, customer_id, date, status)
OrderItem (id, order_id, product_name, quantity, price)
Features:

Create order with multiple items in a single request (nested payload)
Get customer's total spend (sums quantity * price for Confirmed and Shipped orders)
Update order status following transitions: Draft -> Confirmed -> Shipped
Prevent deletion of an order if it's already Shipped
Run locally
Create and activate a virtualenv (recommended):
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
Install requirements:
pip install -r requirements.txt
Start the app:
uvicorn main:app --reload
Open docs at: http://127.0.0.1:8000/docs
Notes
The app uses SQLModel (built on SQLAlchemy) and SQLite database file database.db.
Sample Postman collection is included as postman_collection.json.
