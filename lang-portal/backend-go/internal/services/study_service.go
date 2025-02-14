package services

import (
	"database/sql"
	"lang-portal/internal/models"
	"time"
)

type StudyService struct {
	db *sql.DB
}

func NewStudyService(db *sql.DB) *StudyService {
	return &StudyService{db: db}
}

type StudyActivity struct {
	ID           int    `json:"id"`
	Name         string `json:"name"`
	Description  string `json:"description"`
	ThumbnailURL string `json:"thumbnail_url"`
}

type StudySession struct {
	ID              int       `json:"id"`
	ActivityName    string    `json:"activity_name"`
	GroupName       string    `json:"group_name"`
	StartTime       time.Time `json:"start_time"`
	EndTime         time.Time `json:"end_time"`
	ReviewItemCount int       `json:"review_items_count"`
}

type WordReview struct {
	StudySessionID int       `json:"study_session_id"`
	WordID         int       `json:"word_id"`
	Correct        bool      `json:"correct"`
	CreatedAt      time.Time `json:"created_at"`
}

func (s *StudyService) GetStudyActivity(id int) (*StudyActivity, error) {
	var activity StudyActivity
	err := s.db.QueryRow(`
		SELECT id, name, description, thumbnail_url
		FROM study_activities
		WHERE id = ?`, id).Scan(&activity.ID, &activity.Name, &activity.Description, &activity.ThumbnailURL)
	if err != nil {
		return nil, err
	}
	return &activity, nil
}

func (s *StudyService) GetStudyActivitySessions(activityID, page, itemsPerPage int) ([]StudySession, *PaginationResult, error) {
	var totalItems int
	err := s.db.QueryRow(`
		SELECT COUNT(*)
		FROM study_sessions ss
		WHERE ss.id = ?`, activityID).Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage
	offset := (page - 1) * itemsPerPage

	rows, err := s.db.Query(`
		SELECT 
			ss.id,
			ss.study_activity as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			sa.created_at as end_time,
			COUNT(wri.word_id) as review_items_count
		FROM study_sessions ss
		LEFT JOIN study_activities sa ON ss.id = sa.study_session_id
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		WHERE ss.id = ?
		GROUP BY ss.id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`, activityID, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var sessions []StudySession
	for rows.Next() {
		var session StudySession
		if err := rows.Scan(&session.ID, &session.ActivityName, &session.GroupName, &session.StartTime, &session.EndTime, &session.ReviewItemCount); err != nil {
			return nil, nil, err
		}
		sessions = append(sessions, session)
	}

	pagination := &PaginationResult{
		CurrentPage:  page,
		TotalPages:   totalPages,
		TotalItems:   totalItems,
		ItemsPerPage: itemsPerPage,
	}

	return sessions, pagination, nil
}

func (s *StudyService) GetStudySessions(page, itemsPerPage int) ([]StudySession, *PaginationResult, error) {
	var totalItems int
	err := s.db.QueryRow(`SELECT COUNT(*) FROM study_sessions`).Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage
	offset := (page - 1) * itemsPerPage

	rows, err := s.db.Query(`
		SELECT 
			ss.id,
			ss.study_activity as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			sa.created_at as end_time,
			COUNT(wri.word_id) as review_items_count
		FROM study_sessions ss
		LEFT JOIN study_activities sa ON ss.id = sa.study_session_id
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		GROUP BY ss.id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var sessions []StudySession
	for rows.Next() {
		var session StudySession
		if err := rows.Scan(&session.ID, &session.ActivityName, &session.GroupName, &session.StartTime, &session.EndTime, &session.ReviewItemCount); err != nil {
			return nil, nil, err
		}
		sessions = append(sessions, session)
	}

	pagination := &PaginationResult{
		CurrentPage:  page,
		TotalPages:   totalPages,
		TotalItems:   totalItems,
		ItemsPerPage: itemsPerPage,
	}

	return sessions, pagination, nil
}

func (s *StudyService) GetStudySession(id int) (*StudySession, error) {
	var session StudySession
	err := s.db.QueryRow(`
		SELECT 
			ss.id,
			ss.study_activity as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			sa.created_at as end_time,
			COUNT(wri.word_id) as review_items_count
		FROM study_sessions ss
		LEFT JOIN study_activities sa ON ss.id = sa.study_session_id
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		WHERE ss.id = ?
		GROUP BY ss.id`, id).Scan(&session.ID, &session.ActivityName, &session.GroupName, &session.StartTime, &session.EndTime, &session.ReviewItemCount)
	if err != nil {
		return nil, err
	}
	return &session, nil
}

func (s *StudyService) GetStudySessionWords(sessionID, page, itemsPerPage int) ([]models.Word, *PaginationResult, error) {
	var totalItems int
	err := s.db.QueryRow(`
		SELECT COUNT(DISTINCT w.id)
		FROM words w
		JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wri.study_session_id = ?`, sessionID).Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage
	offset := (page - 1) * itemsPerPage

	rows, err := s.db.Query(`
		SELECT DISTINCT w.id, w.spanish, w.transliteration, w.arabic
		FROM words w
		JOIN word_review_items wri ON w.id = wri.word_id
		WHERE wri.study_session_id = ?
		LIMIT ? OFFSET ?`, sessionID, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var words []models.Word
	for rows.Next() {
		var word models.Word
		if err := rows.Scan(&word.ID, &word.Spanish, &word.Transliteration, &word.Arabic); err != nil {
			return nil, nil, err
		}
		words = append(words, word)
	}

	pagination := &PaginationResult{
		CurrentPage:  page,
		TotalPages:   totalPages,
		TotalItems:   totalItems,
		ItemsPerPage: itemsPerPage,
	}

	return words, pagination, nil
}

func (s *StudyService) CreateStudyActivity(groupID int, activityName string) (int, error) {
	tx, err := s.db.Begin()
	if err != nil {
		return 0, err
	}
	defer tx.Rollback()

	// Create study session first
	result, err := tx.Exec(`
		INSERT INTO study_sessions (group_id, study_activity, created_at)
		VALUES (?, ?, ?)`, groupID, activityName, time.Now())
	if err != nil {
		return 0, err
	}

	sessionID, err := result.LastInsertId()
	if err != nil {
		return 0, err
	}

	// Create study activity linked to session
	_, err = tx.Exec(`
		INSERT INTO study_activities (study_session_id, group_id, created_at)
		VALUES (?, ?, ?)`, sessionID, groupID, time.Now())
	if err != nil {
		return 0, err
	}

	if err := tx.Commit(); err != nil {
		return 0, err
	}

	return int(sessionID), nil
}

func (s *StudyService) ReviewWord(sessionID, wordID int, correct bool) (*WordReview, error) {
	now := time.Now()
	_, err := s.db.Exec(`
		INSERT INTO word_review_items (study_session_id, word_id, correct, created_at)
		VALUES (?, ?, ?, ?)`, sessionID, wordID, correct, now)
	if err != nil {
		return nil, err
	}

	return &WordReview{
		StudySessionID: sessionID,
		WordID:        wordID,
		Correct:       correct,
		CreatedAt:     now,
	}, nil
}

func (s *StudyService) ResetHistory() error {
	_, err := s.db.Exec(`DELETE FROM word_review_items`)
	if err != nil {
		return err
	}

	_, err = s.db.Exec(`DELETE FROM study_sessions`)
	if err != nil {
		return err
	}

	return nil
}

func (s *StudyService) FullReset() error {
	if err := s.ResetHistory(); err != nil {
		return err
	}

	_, err := s.db.Exec(`DELETE FROM word_groups`)
	if err != nil {
		return err
	}

	_, err = s.db.Exec(`DELETE FROM words`)
	if err != nil {
		return err
	}

	_, err = s.db.Exec(`DELETE FROM groups`)
	if err != nil {
		return err
	}

	return nil
}
