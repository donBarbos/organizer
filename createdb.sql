CREATE TABLE IF NOT EXISTS Users(
    user_id INTEGER PRIMARY KEY,
    name VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS WeeklyAffairs(
    user_id INTEGER REFERENCES Users(user_id),
    day INTEGER,
    time INTEGER,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Affairs(
    user_id INTEGER REFERENCES Users(user_id),
    date INTEGER,
    time INTEGER,
    text TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS QuickAffairs(
    user_id INTEGER REFERENCES Users(user_id),
    timer INTEGER,
    text TEXT NOT NULL
);
