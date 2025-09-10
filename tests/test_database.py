import pytest

from src.database import Database
from src.user_table import UserTable


@pytest.fixture
def database(tmp_path):
    db_file = tmp_path / "my_database.db"
    db = Database(str(db_file))
    yield db


@pytest.fixture
def conn_setup(database):
    conn = database._connect()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE user (user_id INTEGER PRIMARY KEY, user_name, user_email, password_hashed, salt , registration_date)"
    )
    yield conn
    conn.close()


@pytest.fixture
def user_table(database):
    return UserTable(database)


@pytest.fixture
def my_user():
    return "Lucas", "my_email@mail.com", "password_salted", "salt", "2012-12-12"


@pytest.fixture
def my_user_dict():
    info_dict = {
        "user_name": "Lucas",
        "user_email": "my_email@mail.com",
        "password_hashed": "password_salted",
        "salt": "salt",
        "registration_date": "2012-12-12",
    }
    return info_dict


def test_add_user(conn_setup, user_table, my_user):
    conn = conn_setup
    cur = conn.cursor()
    user_table.add_user(*my_user)
    cur.execute("SELECT * FROM user")
    result = cur.fetchall()
    assert len(result) == 1
    assert result[0] == (
        1,
        "Lucas",
        "my_email@mail.com",
        "password_salted",
        "salt",
        "2012-12-12",
    )


def test_delete_user(conn_setup, user_table, my_user):
    conn = conn_setup
    cur = conn.cursor()

    user_table.add_user(*my_user)
    delete_row = user_table.delete_user("Not-a-user", "210293")
    assert delete_row is False

    delete_user = user_table.delete_user("Lucas", "my_email@mail.com")
    assert cur.rowcount == -1
    assert delete_user is True

    delete_test = user_table.delete_user("Lucas", "my_email@mail.com")
    assert delete_test is False


def test_select_user(conn_setup, user_table, my_user, my_user_dict):
    _ = conn_setup
    user_table.add_user(*my_user)

    result = user_table.select_user(my_user_dict)
    assert isinstance(result, list)

    user_id, user_name, user_email = result[0]
    assert user_id == 1
    assert user_name == "Lucas"
    assert user_email == "my_email@mail.com"

    wrong_user_info = {
        "user_name": "Sucal",
        "user_email": "my_mail@mail.com",
        "registration_date": "2012-12-12",
    }
    result = user_table.select_user(wrong_user_info)
    assert result is None


def test_update_user(conn_setup, user_table, my_user, my_user_dict):
    _ = conn_setup
    user_table.add_user(*my_user)

    update_info = None
    user_info = {}

    try:
        result = user_table.update_user(update_info, user_info)  # type: ignore
    except TypeError as error:
        assert (
            str(error) == "update_info expected to be a dictionary, but got: NoneType"
        )
    else:
        assert False, "TypeError was not raised"

    update_info = {}
    user_info = None

    try:
        result = user_table.update_user(update_info, user_info)  # type: ignore
    except TypeError as error:
        assert str(error) == "user_info expected to be a dictionary, but got: NoneType"
    else:
        assert False, "TypeError was not raised"

    update_info = {}
    user_info = {"user_id": 1}
    result = user_table.update_user(update_info, user_info)
    assert result is False

    update_info = {"user_id": 1}
    user_info = {}
    result = user_table.update_user(update_info, user_info)
    assert result is False

    update_info = {"user_name": "Sulcas"}
    result = user_table.update_user(update_info, my_user_dict)
    assert result is True

    # UPDATE DATABSE WITH CORRECT user_info
    update_info = {
        "user_name": "Lucas",
        "user_email": "fake@mail.com",
        "registration_date": "2012-12-12",
    }
    user_info = {
        "user_name": "Sulcas",
        "user_email": "my_email@mail.com",
        "registration_date": "2012-12-12",
    }
    result = user_table.update_user(update_info, user_info)
    assert result is True

    # TEST UPDATE DATABASE WITH WRONG user_info
    update_info = {
        "user_name": "Lucas",
    }
    user_info = {
        "user_name": "Sulcas",
        "user_email": "my_email@mail.com",
        "registration_date": "2020-12-12",
    }
    result = user_table.update_user(update_info, user_info)
    assert result is False
