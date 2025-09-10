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
