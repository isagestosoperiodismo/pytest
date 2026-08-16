import pytest
import os

from order_service import calculate_and_save_order
from database import OrderDatabase


@pytest.fixture
def test_db():
    """Create a test database that is cleaned up after tests."""
    db_path = "test_orders.db"
    db = OrderDatabase(db_path)
    yield db
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


class TestOrderDatabase:
    def test_save_and_retrieve_order_without_discount(self, test_db):
        """Test saving and retrieving order without discount."""
        items = [{'price': 50.0, 'quantity': 1}]
        total, order_id = calculate_and_save_order(items, apply_discount=False, db_path="test_orders.db")
        
        order = test_db.get_order(order_id)
        assert order is not None
        assert order['total'] == 50.0
        assert order['discount_applied'] == 0
        assert len(order['items']) == 1
        assert order['items'][0]['price'] == 50.0
        assert order['items'][0]['quantity'] == 1
    
    def test_save_and_retrieve_order_with_discount(self, test_db):
        """Test saving and retrieving order with discount."""
        items = [{'price': 50.0, 'quantity': 1}]
        total, order_id = calculate_and_save_order(items, apply_discount=True, db_path="test_orders.db")
        
        order = test_db.get_order(order_id)
        assert order is not None
        assert order['total'] == 45.0
        assert order['discount_applied'] == 1
    
    def test_save_multiple_items_order(self, test_db):
        """Test saving order with multiple items."""
        items = [
            {'price': 50.0, 'quantity': 1},
            {'price': 25.0, 'quantity': 2}
        ]
        total, order_id = calculate_and_save_order(items, apply_discount=False, db_path="test_orders.db")
        
        order = test_db.get_order(order_id)
        assert order is not None
        assert order['total'] == 100.0
        assert len(order['items']) == 2
    
    def test_get_all_orders(self, test_db):
        """Test retrieving all orders."""
        items1 = [{'price': 50.0, 'quantity': 1}]
        items2 = [{'price': 100.0, 'quantity': 2}]
        
        calculate_and_save_order(items1, apply_discount=False, db_path="test_orders.db")
        calculate_and_save_order(items2, apply_discount=True, db_path="test_orders.db")
        
        all_orders = test_db.get_all_orders()
        assert len(all_orders) == 2
        assert all_orders[0]['total'] == 50.0
        assert all_orders[1]['total'] == 180.0  # 200 * 0.9
    
    def test_order_id_increments(self, test_db):
        """Test that order IDs increment correctly."""
        items = [{'price': 50.0, 'quantity': 1}]
        
        _, order_id_1 = calculate_and_save_order(items, apply_discount=False, db_path="test_orders.db")
        _, order_id_2 = calculate_and_save_order(items, apply_discount=False, db_path="test_orders.db")
        
        assert order_id_2 == order_id_1 + 1
