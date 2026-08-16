import os
from fastapi.testclient import TestClient

from api_server import app


def test_create_user_and_order(tmp_path):
    db_path = str(tmp_path / "api_test.db")

    client = TestClient(app)

    # Create user
    resp = client.post("/users", json={"username": "apiuser", "email": "api@local"}, params={"db_path": db_path})
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["username"] == "apiuser"

    # Create order
    payload = {"items": [{"price": 50.0, "quantity": 1}], "apply_discount": False}
    resp = client.post("/orders", json=payload, params={"db_path": db_path})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 50.0
    order_id = data["id"]

    # Retrieve order
    resp = client.get(f"/orders/{order_id}", params={"db_path": db_path})
    assert resp.status_code == 200
    order = resp.json()
    assert order["total"] == 50.0
    assert order["items"][0]["price"] == 50.0
