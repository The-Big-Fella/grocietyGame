CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    round_number INTEGER NOT NULL,

    FOREIGN KEY (event_id) REFERENCES events(id)
);


CREATE TABLE IF NOT EXISTS question_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    type_id INTEGER NOT NULL,

    text TEXT NOT NULL,
    budget INTEGER NOT NULL,
    mood INTEGER NOT NULL,

    FOREIGN KEY (round_id) REFERENCES rounds(id),
    FOREIGN KEY (type_id) REFERENCES question_types(id)
);


CREATE INDEX IF NOT EXISTS idx_rounds_event_id
    ON rounds(event_id);

CREATE INDEX IF NOT EXISTS idx_questions_round_id
    ON questions(round_id);

CREATE INDEX IF NOT EXISTS idx_questions_type_id
    ON questions(type_id);
