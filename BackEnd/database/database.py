from database.database_manager import DatabaseManager


class Database(DatabaseManager):
    def __init__(self):
        super().__init__()

    def create_event(self, name: str):
        with self.transaction() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO events (name) VALUES (?)",
                (name,)
            )

    def get_events(self):
        with self.transaction() as conn:
            return [dict(r) for r in conn.execute(
                "SELECT * FROM events ORDER BY name"
            )]

    def create_question_type(self, name: str):
        with self.transaction() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO question_types (name) VALUES (?)",
                (name,)
            )

    def get_question_types(self):
        with self.transaction() as conn:
            return [dict(r) for r in conn.execute(
                "SELECT * FROM question_types ORDER BY name"
            )]

    def create_round(self, event_name: str, round_number: int) -> int:
        with self.transaction() as conn:
            event_id = conn.execute(
                "SELECT id FROM events WHERE name = ?",
                (event_name,)
            ).fetchone()

            if not event_id:
                raise ValueError(f"Unknown event: {event_name}")

            cur = conn.execute(
                """
                INSERT INTO rounds (event_id, round_number)
                VALUES (?, ?)
                """,
                (event_id["id"], round_number)
            )
            return cur.lastrowid

    def get_rounds(self):
        with self.transaction() as conn:
            return [dict(r) for r in conn.execute("""
                SELECT
                    r.id,
                    r.round_number,
                    e.name AS event
                FROM rounds r
                JOIN events e ON r.event_id = e.id
                ORDER BY r.round_number
            """)]

    def add_question(
        self,
        round_id: int,
        type_name: str,
        text: str,
        budget: int,
        mood: int
    ):
        with self.transaction() as conn:
            # Enforce max 3 questions per round
            count = conn.execute(
                "SELECT COUNT(*) AS c FROM questions WHERE round_id = ?",
                (round_id,)
            ).fetchone()["c"]

            if count >= 3:
                raise ValueError("A round can only have 3 questions")

            type_id = conn.execute(
                "SELECT id FROM question_types WHERE name = ?",
                (type_name,)
            ).fetchone()

            if not type_id:
                raise ValueError(f"Unknown question type: {type_name}")

            conn.execute(
                """
                INSERT INTO questions (round_id, type_id, text, budget, mood)
                VALUES (?, ?, ?, ?, ?)
                """,
                (round_id, type_id["id"], text, budget, mood)
            )

    def get_questions(self):
        with self.transaction() as conn:
            return [dict(r) for r in conn.execute("""
                SELECT
                    q.id,
                    q.text,
                    q.budget,
                    q.mood,
                    qt.name AS type,
                    r.round_number,
                    e.name AS event
                FROM questions q
                JOIN question_types qt ON q.type_id = qt.id
                JOIN rounds r ON q.round_id = r.id
                JOIN events e ON r.event_id = e.id
                ORDER BY r.round_number, q.id
            """)]

    def get_questions_for_round(self, round_number: int):
        with self.transaction() as conn:
            rows = conn.execute("""
                SELECT
                    q.id,
                    q.text,
                    q.budget,
                    q.mood,
                    qt.name AS type
                FROM questions q
                JOIN question_types qt ON q.type_id = qt.id
                JOIN rounds r ON q.round_id = r.id
                WHERE r.round_number = ?
                ORDER BY q.id
            """, (round_number,)).fetchall()

            if len(rows) != 3:
                raise ValueError(
                    f"Round {round_number} has {len(rows)} questions"
                )

            return [dict(r) for r in rows]
