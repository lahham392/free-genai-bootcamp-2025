-- +goose Up
ALTER TABLE study_sessions ADD COLUMN created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;

-- +goose Down
ALTER TABLE study_sessions DROP COLUMN created_at;
