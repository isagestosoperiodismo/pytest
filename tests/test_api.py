import os
from fastapi.testclient import TestClient

from api_server import app


def test_api_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "message" in data


def test_create_user_and_order_with_sqlite(tmp_path):
    db_path = str(tmp_path / "api_test.db")

    client = TestClient(app)

    resp = client.post("/users", json={"username": "apiuser", "email": "api@local"}, params={"db_path": db_path})
    assert resp.status_code == 200
    data = resp.json()
    assert "id" in data
    assert data["username"] == "apiuser"

    payload = {"items": [{"price": 50.0, "quantity": 1}], "apply_discount": False}
    resp = client.post("/orders", json=payload, params={"db_path": db_path})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 50.0
    order_id = data["id"]

    resp = client.get(f"/orders/{order_id}", params={"db_path": db_path})
    assert resp.status_code == 200
    order = resp.json()
    assert order["total"] == 50.0
    assert order["items"][0]["price"] == 50.0


def test_create_user_and_order_with_json(tmp_path):
    json_path = str(tmp_path / "api_test.json")

    client = TestClient(app)

    resp = client.post("/users", json={"username": "jsonuser", "email": "json@local"}, params={"db_path": json_path})
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "jsonuser"
    assert data["id"] == 1

    payload = {"items": [{"price": 100.0, "quantity": 2}], "apply_discount": True}
    resp = client.post("/orders", json=payload, params={"db_path": json_path})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 180.0
    order_id = data["id"]

    resp = client.get(f"/orders/{order_id}", params={"db_path": json_path})
    assert resp.status_code == 200
    order = resp.json()
    assert order["total"] == 180.0
    assert order["discount_applied"] is True


def test_get_user_validation_not_found(tmp_path):
    json_path = str(tmp_path / "api_test.json")
    client = TestClient(app)

    resp = client.get(f"/users/someuser", params={"db_path": json_path})
    assert resp.status_code == 404
    data = resp.json()
    assert "detail" in data


def test_get_user_success(tmp_path):
    json_path = str(tmp_path / "api_test.json")
    client = TestClient(app)

    # create user
    resp = client.post("/users", json={"username": "ana", "email": "ana@test.com"}, params={"db_path": json_path})
    assert resp.status_code == 200

    resp = client.get("/users/ana", params={"db_path": json_path})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data.get("id"), int)
    assert isinstance(data.get("username"), str)
    assert "email" in data

