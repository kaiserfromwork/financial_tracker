import sqlite3


class Database:
    def __init__(self, db_path: str):
        if not isinstance(db_path, str):
            raise TypeError("Not a valid database path.")
        if not db_path.endswith(".db"):
            raise ValueError("Not a valid database file.")
        self.db_path = db_path

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def add_user(self, name, email, password_hashed, salt, registration_date):
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO user (user_name, user_email, password_hashed, salt, registration_date)
                VALUES (?, ?, ?, ?, ?)
                """,
                (name, email, password_hashed, salt, registration_date),
            )
