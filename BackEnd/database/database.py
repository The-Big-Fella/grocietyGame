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
                    r.event_id,
                    r.round_number,
                    e.name AS event
                FROM rounds r
                JOIN events e ON r.event_id = e.id
                ORDER BY r.round_number
            """)]

    def add_question(self, round_id: int, type_id: int, text: str, budget: int, mood: int):
        with self.transaction() as conn:
            # Check limit
            count = conn.execute(
                "SELECT COUNT(*) as c FROM questions WHERE round_id = ?", (round_id,)).fetchone()["c"]
            if count >= 3:
                raise ValueError("A round can only have 3 questions")

            conn.execute("""
                INSERT INTO questions (round_id, type_id, text, budget, mood)
                VALUES (?, ?, ?, ?, ?)
            """, (round_id, type_id, text, budget, mood))

    def get_questions_for_round(self, event_id: int, round_number: int):
        with self.transaction() as conn:
            rows = conn.execute("""
                    SELECT q.id, q.text, q.budget, q.mood, qt.name AS type
                    FROM questions q
                    JOIN question_types qt ON q.type_id = qt.id
                    JOIN rounds r ON q.round_id = r.id
                    WHERE r.event_id = ? AND r.round_number = ?
                    ORDER BY q.id
                """, (event_id, round_number)).fetchall()

            if len(rows) != 3:
                raise ValueError(
                    f"Round {round_number} has {len(rows)} questions"
                )

            return [dict(r) for r in rows]

    def get_questions_by_round(self, round_id):
        with self.transaction() as conn:
            cursor = conn.execute("""
                select text, budget, mood 
                from questions 
                where round_id = ?
            """, (round_id,))
            return [dict(row) for row in cursor.fetchall()]

    def get_questions(self):
        try:
            with self.transaction() as conn:
                # Use LEFT JOIN so questions show up even if type_id is broken
                cursor = conn.execute("""
                        SELECT 
                            q.id, 
                            q.round_id, 
                            qt.name AS type_name, 
                            q.text, 
                            q.budget, 
                            q.mood 
                        FROM questions q 
                        LEFT JOIN question_types qt ON q.type_id = qt.id
                    """)
                return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            # This is where the "no such column" error is hiding!
            print(f"DATABASE ERROR: {e}")
            return []

    def delete_question(self, question_id: int):
        with self.transaction() as conn:
            conn.execute(
                "DELETE FROM questions WHERE id = ?", (question_id,))

    def update_question(self, question_id: int, text: str, budget: int, mood: int):
        with self.transaction() as conn:
            conn.execute("""
                UPDATE questions 
                SET text = COALESCE(?, text), 
                    budget = COALESCE(?, budget), 
                    mood = COALESCE(?, mood)
                WHERE id = ?
            """, (text, budget, mood, question_id))

    def add_event(self, name: str):
        with self.transaction() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO events (name) VALUES (?)", (name,))

    def update_event(self, event_id: int, name: str):
        with self.transaction() as conn:
            conn.execute("UPDATE events SET name = ? WHERE id = ?",
                         (name, event_id))

    def delete_event(self, event_id: int):
        with self.transaction() as conn:
            conn.execute("DELETE FROM events WHERE id = ?", (event_id,))

    def add_round(self, event_id: int, round_number: int):
        with self.transaction() as conn:
            cur = conn.execute(
                "INSERT INTO rounds (event_id, round_number) VALUES (?, ?)",
                (event_id, round_number)
            )
            return cur.lastrowid

    def delete_round(self, round_id: int):
        with self.transaction() as conn:
            conn.execute("DELETE FROM rounds WHERE id = ?", (round_id,))
