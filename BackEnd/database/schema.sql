CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS question_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,
    -- If an event is deleted, delete its rounds too
    FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE,
    UNIQUE(event_id, round_number)
);

CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    budget INTEGER NOT NULL,
    mood INTEGER NOT NULL,
    -- Safety: If a round is deleted, delete its questions too
    FOREIGN KEY (round_id) REFERENCES rounds (id) ON DELETE CASCADE,
    FOREIGN KEY (type_id) REFERENCES question_types (id),
    -- Optional: Ensure mood stays within a realistic range
    CHECK (mood BETWEEN -100 AND 100)
);

-- Speed up lookups for questions within a round
CREATE INDEX IF NOT EXISTS idx_questions_round_id ON questions(round_id);
