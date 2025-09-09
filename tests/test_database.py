import sqlite3
import pytest
import os

from src.database import Database


@pytest.fixture
def test_db_conn(tmp_path):
    db_file = tmp_path / "my_database.db"
    db = Database(str(db_file))
    conn = db._connect()
    yield conn
    conn.close()


def delete_temp_db(temp_db):
    if os.path.exists(temp_db):
        os.remove(temp_db)


def test_connect(test_db_conn):
    conn = test_db_conn
    assert isinstance(conn, sqlite3.Connection)

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    assert result[0] == 1

    conn.close()


def test_add_user(tmp_path):
    db_file = tmp_path / "my_database.db"
    db = Database(str(db_file))
    with db._connect() as conn:
        assert isinstance(conn, sqlite3.Connection)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt , registration_date)"
        )
        db.add_user(
            "Lucas", "my_email@mail.com", "password_salted", "password_salt", "12-12-12"
        )
        cur.execute("SELECT * FROM user")
        result = cur.fetchall()
        assert len(result) == 1

        delete_temp_db("my_database.db")


def test_delete_user(tmp_path):
    db_file = tmp_path / "my_database.db"
    db = Database(str(db_file))
    with db._connect() as conn:
        assert isinstance(conn, sqlite3.Connection)

        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt, registration_date)
        """)

        db.add_user("Lucas", "my_email@mail.com", "password_salted", "salt", "20-20-20")
        delete_row = db.delete_user("Not-a-user", "210293")
        assert delete_row is False

        delete_user = db.delete_user("Lucas", "my_email@mail.com")
        assert cur.rowcount == -1
        assert delete_user is True

        delete_test = db.delete_user("Lucas", "my_email@mail.com")
        assert delete_test is False

        delete_temp_db("my_database.db")


def test_select_user(tmp_path):
    db_file = tmp_path / "my_database.db"
    db = Database(str(db_file))
    with db._connect() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt, registration_date)
        """)
        db.add_user("Lucas", "my_email@mail.com", "password_salted", "salt", "20-20-20")

        user_info = {
            "user_name": "Lucas",
            "user_email": "my_email@mail.com",
            "registration_date": "20-20-20",
        }
        result = db.select_user(user_info)
        assert isinstance(result, list)

        user_id, user_name, user_email = result[0]
        assert user_id == 1
        assert user_name == "Lucas"
        assert user_email == "my_email@mail.com"

        wrong_user_info = {
            "user_name": "Sucal",
            "user_email": "my_mail@mail.com",
            "registration_date": "10-20-20",
        }
        result = db.select_user(wrong_user_info)
        assert result is None

        delete_temp_db("my_database.db")
