import sqlite3
import pytest

from src.database import Database


@pytest.fixture
def test_db_conn():
    db = Database("my_database.db")
    conn = db._connect()
    yield conn
    conn.close()


def test_connect(test_db_conn):
    conn = test_db_conn
    assert isinstance(conn, sqlite3.Connection)

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    assert result[0] == 1

    conn.close()


def test_add_user():
    db = Database("my_database.db")
    with db._connect() as conn:
        assert isinstance(conn, sqlite3.Connection)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE user (user_name, user_email, password_hashed, salt , registration_date)"
        )
        db.add_user(
            "Lucas", "my_email@mail.com", "password_salted", "password_salt", "12-12-12"
        )
        cur.execute("SELECT * FROM user")
        result = cur.fetchall()
        assert len(result) == 1
