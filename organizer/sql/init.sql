CREATE TABLE IF NOT EXISTS Users(
    user_id BIGSERIAL PRIMARY KEY,
    name VARCHAR(32),
    lang VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS Notes(
    user_id BIGSERIAL REFERENCES Users (user_id),
    note_id BIGSERIAL,
    date_time TIMESTAMP,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS WeeklyNotes(
    user_id BIGSERIAL REFERENCES Users (user_id),
    note_id BIGSERIAL,
    weekday VARCHAR(1),
    time TIME,
    text TEXT NOT NULL
);
