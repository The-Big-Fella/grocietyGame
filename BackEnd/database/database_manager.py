import sqlite3
import os
from contextlib import contextmanager


class DatabaseManager:
    def __init__(self, db_path: str = "game.db"):
        self.db_path = db_path

        db_exists = os.path.exists(self.db_path)

        if not db_exists:
            # print(f"Database {
            #       self.db_path} not found. Creating and initializing...")
            self._initialize_schema()
        else:
            self._initialize_schema()

        with self.transaction() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO question_types (id, name) VALUES (1, 'Choice')")
            conn.execute(
                "INSERT OR IGNORE INTO question_types (id, name) VALUES (2, 'Action')")

            print("Database lookup tables initialized.")

    def _initialize_schema(self):
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

        if not os.path.exists(schema_path):
            print(f"Warning: Schema file not found at {schema_path}")
            return

        with open(schema_path, 'r') as f:
            schema_sql = f.read()

        with self.transaction() as conn:
            conn.executescript(schema_sql)

    @contextmanager
    def transaction(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
