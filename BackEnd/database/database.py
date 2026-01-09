from database.database_manager import DatabaseManager


class Database(DatabaseManager):
    def __init__(self):
        super().__init__()

    def get_questions(self):
        with self.transaction() as conn:
            cursor = conn.cursor()
