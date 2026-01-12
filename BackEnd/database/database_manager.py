from pathlib import Path
import sqlite3
from contextlib import contextmanager


class DatabaseManager():
    def __init__(self, path="./database/database.db"):
        base_dir = Path(__file__).resolve().parent

        self.db_path = base_dir / "database.db"
        self.schema_path = base_dir / "schema.sql"
        self.apply_schema()

    @contextmanager
    def transaction(self):
        self.con = sqlite3.connect(self.db_path)
        try:
            yield self.con
            self.con.commit()
        except Exception:
            self.con.rollback()
            raise
        finally:
            self.con.close()

    def apply_schema(self):
        if not self.schema_path.exists():
            raise FileNotFoundError(
                f"Schema file not found: {self.schema_path}")

        schema_sql = self.schema_path.read_text(encoding="utf-8")

        with self.transaction() as conn:
            conn.executescript(schema_sql)
