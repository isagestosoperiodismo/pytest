import sqlite3
import json
import os
from typing import List, Dict, Optional


class OrderDatabase:
    
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path
        self.is_json = db_path.endswith(".json")
        self.init_db()
    
    def init_db(self):
        if self.is_json:
            self._init_json()
        else:
            self._init_sqlite()
    
    def _init_json(self):
        if not os.path.exists(self.db_path):
            data = {"users": [], "orders": [], "next_user_id": 1, "next_order_id": 1}
            os.makedirs(os.path.dirname(self.db_path) or ".", exist_ok=True)
            with open(self.db_path, "w") as f:
                json.dump(data, f, indent=2)
    
    def _init_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total REAL NOT NULL,
                    discount_applied INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL
                )
            """)
            conn.commit()
    
    def save_order(self, items: List[Dict], total: float, discount_applied: bool) -> int:
        if self.is_json:
            return self._save_order_json(items, total, discount_applied)
        else:
            return self._save_order_sqlite(items, total, discount_applied)
    
    def _save_order_json(self, items: List[Dict], total: float, discount_applied: bool) -> int:
        with open(self.db_path, "r") as f:
            data = json.load(f)
        
        order_id = data["next_order_id"]
        order = {
            "id": order_id,
            "total": total,
            "discount_applied": discount_applied,
            "items": items
        }
        data["orders"].append(order)
        data["next_order_id"] += 1
        
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return order_id
    
    def _save_order_sqlite(self, items: List[Dict], total: float, discount_applied: bool) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (total, discount_applied) VALUES (?, ?)",
                (total, 1 if discount_applied else 0)
            )
            order_id = cursor.lastrowid
            
            for item in items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, price, quantity) VALUES (?, ?, ?)",
                    (order_id, item['price'], item['quantity'])
                )
            
            conn.commit()
            return order_id
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        if self.is_json:
            return self._get_order_json(order_id)
        else:
            return self._get_order_sqlite(order_id)
    
    def _get_order_json(self, order_id: int) -> Optional[Dict]:
        with open(self.db_path, "r") as f:
            data = json.load(f)
        
        for order in data["orders"]:
            if order["id"] == order_id:
                return order
        return None
    
    def _get_order_sqlite(self, order_id: int) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            order = cursor.fetchone()
            
            if not order:
                return None
            
            cursor.execute("SELECT price, quantity FROM order_items WHERE order_id = ?", (order_id,))
            items = [dict(row) for row in cursor.fetchall()]
            
            return {
                'id': order['id'],
                'total': order['total'],
                'discount_applied': order['discount_applied'],
                'items': items,
                'created_at': order['created_at']
            }
    
    def get_all_orders(self) -> List[Dict]:
        if self.is_json:
            return self._get_all_orders_json()
        else:
            return self._get_all_orders_sqlite()
    
    def _get_all_orders_json(self) -> List[Dict]:
        with open(self.db_path, "r") as f:
            data = json.load(f)
        return data["orders"]
    
    def _get_all_orders_sqlite(self) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders")
            orders = [dict(row) for row in cursor.fetchall()]
            return orders
    
    def clear_database(self):
        if self.is_json:
            self._clear_json()
        else:
            self._clear_sqlite()
    
    def _clear_json(self):
        data = {"users": [], "orders": [], "next_user_id": 1, "next_order_id": 1}
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def _clear_sqlite(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items")
            cursor.execute("DELETE FROM orders")
            conn.commit()

    def save_user(self, username: str, email: str) -> int:
        if self.is_json:
            return self._save_user_json(username, email)
        else:
            return self._save_user_sqlite(username, email)
    
    def _save_user_json(self, username: str, email: str) -> int:
        with open(self.db_path, "r") as f:
            data = json.load(f)
        
        user_id = data["next_user_id"]
        user = {"id": user_id, "username": username, "email": email}
        data["users"].append(user)
        data["next_user_id"] += 1
        
        with open(self.db_path, "w") as f:
            json.dump(data, f, indent=2)
        
        return user_id
    
    def _save_user_sqlite(self, username: str, email: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
            conn.commit()
            return cursor.lastrowid

    def get_user_by_username(self, username: str) -> Optional[Dict]:
        if self.is_json:
            return self._get_user_by_username_json(username)
        else:
            return self._get_user_by_username_sqlite(username)
    
    def _get_user_by_username_json(self, username: str) -> Optional[Dict]:
        with open(self.db_path, "r") as f:
            data = json.load(f)
        
        for user in data["users"]:
            if user["username"] == username:
                return user
        return None
    
    def _get_user_by_username_sqlite(self, username: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
