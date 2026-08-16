from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

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


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}


@app.post("/users")
def create_user(user: UserCreate, db_path: Optional[str] = Query("orders.db")):
    db = OrderDatabase(db_path)
    try:
        user_id = db.save_user(user.username, user.email)
        return {"id": user_id, "username": user.username}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users")
def list_users(db_path: Optional[str] = Query("data/users.json")):
    db = OrderDatabase(db_path)
    try:
        if db.is_json:
            import json
            with open(db.db_path, "r") as f:
                data = json.load(f)
            return {"users": data.get("users", [])}
        else:
            with __import__("sqlite3").connect(db.db_path) as conn:
                conn.row_factory = __import__("sqlite3").Row
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, email FROM users")
                users = [dict(row) for row in cursor.fetchall()]
                return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{username}")
def get_user(username: str, db_path: Optional[str] = Query("data/users.json")):
    db = OrderDatabase(db_path)
    user = db.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
