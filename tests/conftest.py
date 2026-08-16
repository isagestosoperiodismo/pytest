import os
import sqlite3
import pytest

from database import OrderDatabase


@pytest.fixture
def single_item():
    return [{'price': 50.0, 'quantity': 1}]


@pytest.fixture
def multiple_items():
    return [
        {'price': 50.0, 'quantity': 1},
        {'price': 25.0, 'quantity': 2}
    ]


@pytest.fixture
def db_connection(tmp_path):
    """Create a temporary sqlite database and return a connection."""
    db_path = str(tmp_path / "test_db.sqlite")
    # Initialize DB schema via OrderDatabase
    OrderDatabase(db_path)
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()
    try:
        os.remove(db_path)
    except OSError:
        pass
