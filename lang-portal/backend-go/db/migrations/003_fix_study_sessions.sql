-- Fix study sessions schema

-- Drop existing tables that depend on study_sessions
DROP TABLE IF EXISTS word_review_items;
DROP TABLE IF EXISTS study_sessions;

-- Recreate study_sessions table with group_id
CREATE TABLE IF NOT EXISTS study_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    study_activity_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    start_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time DATETIME,
    FOREIGN KEY (study_activity_id) REFERENCES study_activities(id),
    FOREIGN KEY (group_id) REFERENCES groups(id)
);

-- Recreate word_review_items table
CREATE TABLE IF NOT EXISTS word_review_items (
    word_id INTEGER NOT NULL,
    study_session_id INTEGER NOT NULL,
    correct BOOLEAN NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (study_session_id) REFERENCES study_sessions(id),
    PRIMARY KEY (word_id, study_session_id)
);
