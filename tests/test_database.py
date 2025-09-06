import sqlite3
import pytest

from src.database import Database


@pytest.fixture
def db_conn():
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()


def test_connect():
    db = Database("my_database.db")
    conn = db._connect()

    assert isinstance(conn, sqlite3.Connection)

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    assert result[0] == 1

    conn.close()
