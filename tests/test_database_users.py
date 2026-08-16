import pytest

from database import OrderDatabase


def test_save_and_get_user(tmp_path):
    db_path = str(tmp_path / "users_test.db")
    db = OrderDatabase(db_path)

    user_id = db.save_user("alice", "alice@example.com")
    assert isinstance(user_id, int)

    user = db.get_user_by_username("alice")
    assert user is not None
    assert user['username'] == "alice"
    assert user['email'] == "alice@example.com"

    # Non existing user
    assert db.get_user_by_username("bob") is None


def test_save_user_via_connection(db_connection):
    """Use the raw sqlite connection fixture to save a user and query it."""
    conn = db_connection
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?)", ("ana", "ana@test.com"))
    conn.commit()

    cursor.execute("SELECT username FROM users WHERE username = ?", ("ana",))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == "ana"
