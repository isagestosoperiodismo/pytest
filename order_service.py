from main import calculate_order_total
from database import OrderDatabase


def calculate_and_save_order(items, apply_discount=False, db_path="orders.db"):


    total = calculate_order_total(items, apply_discount)
    

    db = OrderDatabase(db_path)
    order_id = db.save_order(items, total, apply_discount)
    
    return total, order_id
