from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from models import OrderCreate, UserCreate
from order_service import calculate_and_save_order
from database import OrderDatabase

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users")
def create_user(user: UserCreate, db_path: Optional[str] = Query("orders.db")):
    db = OrderDatabase(db_path)
    try:
        user_id = db.save_user(user.username, user.email)
        return {"id": user_id, "username": user.username}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/orders")
def create_order(order: OrderCreate, db_path: Optional[str] = Query("orders.db")):
    try:
        total, order_id = calculate_and_save_order(order.items, order.apply_discount, db_path)
        return {"id": order_id, "total": total}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders/{order_id}")
def get_order(order_id: int, db_path: Optional[str] = Query("orders.db")):
    db = OrderDatabase(db_path)
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
