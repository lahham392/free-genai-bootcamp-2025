-- +goose Up
-- First drop the foreign key constraints
DROP TABLE IF EXISTS word_review_items;
DROP TABLE IF EXISTS study_activities;
DROP TABLE IF EXISTS study_sessions;

-- Recreate study_sessions table
CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    group_id INTEGER NOT NULL,
    study_activity TEXT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Recreate study_activities table
CREATE TABLE study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_session_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Recreate word_review_items table
CREATE TABLE word_review_items (
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id),
    PRIMARY KEY (word_id, study_session_id)
);

-- +goose Down
DROP TABLE IF EXISTS word_review_items;
DROP TABLE IF EXISTS study_activities;
DROP TABLE IF EXISTS study_sessions;

-- Restore previous schema
CREATE TABLE study_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity_name TEXT NOT NULL,
    group_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_activity_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    start_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

CREATE TABLE word_review_items (
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id),
    PRIMARY KEY (word_id, study_session_id)
);
