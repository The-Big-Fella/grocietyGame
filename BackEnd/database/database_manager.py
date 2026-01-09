import sqlite3

from contextlib import contextmanager


class DatabaseManager():
    def __init__(self, path="./database/database.db"):
        self.path = path

    @contextmanager
    def transaction(self):
        self.con = sqlite3.connect(self.path)
        try:
            yield self.con
        finally:
            self.conn.close()
