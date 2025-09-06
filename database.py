import sqlite3


class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect("finance.db")
