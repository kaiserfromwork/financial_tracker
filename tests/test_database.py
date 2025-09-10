import sqlite3
import pytest

from src.database import Database
from src.user_table import UserTable


@pytest.fixture
def database(tmp_path):
    db_file = tmp_path / "my_database.db"
    db = Database(str(db_file))
    return db


def test_add_user(database):
    db = database
    user_table = UserTable(database)
    with db._connect() as conn:
        assert isinstance(conn, sqlite3.Connection)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt , registration_date)"
        )
        user_table.add_user(
            "Lucas", "my_email@mail.com", "password_salted", "password_salt", "12-12-12"
        )
        cur.execute("SELECT * FROM user")
        result = cur.fetchall()
        assert len(result) == 1


def test_delete_user(database):
    db = database
    user_table = UserTable(database)
    with db._connect() as conn:
        assert isinstance(conn, sqlite3.Connection)

        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt, registration_date)
        """)

        user_table.add_user(
            "Lucas", "my_email@mail.com", "password_salted", "salt", "20-20-20"
        )
        delete_row = user_table.delete_user("Not-a-user", "210293")
        assert delete_row is False

        delete_user = user_table.delete_user("Lucas", "my_email@mail.com")
        assert cur.rowcount == -1
        assert delete_user is True

        delete_test = user_table.delete_user("Lucas", "my_email@mail.com")
        assert delete_test is False


def test_select_user(database):
    db = database
    user_table = UserTable(database)
    with db._connect() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt, registration_date)
        """)
        user_table.add_user(
            "Lucas", "my_email@mail.com", "password_salted", "salt", "20-20-20"
        )

        user_info = {
            "user_name": "Lucas",
            "user_email": "my_email@mail.com",
            "registration_date": "20-20-20",
        }
        result = user_table.select_user(user_info)
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
        result = user_table.select_user(wrong_user_info)
        assert result is None
