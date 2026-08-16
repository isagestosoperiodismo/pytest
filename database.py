import sqlite3
from typing import List, Dict


class OrderDatabase:
    
    def __init__(self, db_path: str = "orders.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
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
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Insert order
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
    
    def get_order(self, order_id: int) -> Dict:
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
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM orders")
            orders = [dict(row) for row in cursor.fetchall()]
            
            return orders
    
    def clear_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM order_items")
            cursor.execute("DELETE FROM orders")
            conn.commit()

    # --- User helper methods ---
    def save_user(self, username: str, email: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", (username, email))
            conn.commit()
            return cursor.lastrowid

    def get_user_by_username(self, username: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
