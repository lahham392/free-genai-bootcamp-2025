package services

import (
	"database/sql"
	"time"
)

type DashboardService struct{
	db *sql.DB
}

func NewDashboardService(db *sql.DB) *DashboardService {
	return &DashboardService{db: db}
}

type LastStudySession struct {
	ID              int       `json:"id"`
	CreatedAt       time.Time `json:"created_at"`
	GroupID         int       `json:"group_id"`
	GroupName       string    `json:"group_name"`
	StudyActivityID string    `json:"study_activity_id"`
	WordCount       int       `json:"word_count"`
	CorrectCount    int       `json:"correct_count"`
	Accuracy        float64   `json:"accuracy"`
}

type StudyProgress struct {
	TotalWordsStudied    int `json:"total_words_studied"`
	TotalAvailableWords int `json:"total_available_words"`
}

type QuickStats struct {
	SuccessRate        float64 `json:"success_rate"`
	TotalStudySessions int     `json:"total_study_sessions"`
	TotalActiveGroups  int     `json:"total_active_groups"`
	StudyStreakDays    int     `json:"study_streak_days"`
}

func (s *DashboardService) GetLastStudySession() (*LastStudySession, error) {
	var session LastStudySession
	err := s.db.QueryRow(`
		SELECT 
			ss.id,
			ss.created_at,
			ss.group_id,
			g.name as group_name,
			ss.study_activity,
			COUNT(DISTINCT wri.word_id) as word_count,
			SUM(CASE WHEN wri.correct THEN 1 ELSE 0 END) as correct_count
		FROM study_sessions ss
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		GROUP BY ss.id
		ORDER BY ss.created_at DESC
		LIMIT 1
	`).Scan(
		&session.ID,
		&session.CreatedAt,
		&session.GroupID,
		&session.GroupName,
		&session.StudyActivityID,
		&session.WordCount,
		&session.CorrectCount,
	)
	if err != nil {
		return nil, err
	}

	if session.WordCount > 0 {
		session.Accuracy = float64(session.CorrectCount) / float64(session.WordCount) * 100
	}

	return &session, nil
}

func (s *DashboardService) GetStudyProgress() (*StudyProgress, error) {
	var progress StudyProgress

	// Get total words studied (unique words that have been reviewed)
	err := s.db.QueryRow(`
		SELECT COUNT(DISTINCT word_id)
		FROM word_review_items
	`).Scan(&progress.TotalWordsStudied)
	if err != nil {
		return nil, err
	}

	// Get total available words
	err = DB.QueryRow(`
		SELECT COUNT(*)
		FROM words
	`).Scan(&progress.TotalAvailableWords)
	if err != nil {
		return nil, err
	}

	return &progress, nil
}

func (s *DashboardService) GetQuickStats() (*QuickStats, error) {
	var stats QuickStats

	// Get success rate
	err := s.db.QueryRow(`
		SELECT COALESCE(AVG(CASE WHEN correct THEN 100.0 ELSE 0.0 END), 0)
		FROM word_review_items
	`).Scan(&stats.SuccessRate)
	if err != nil {
		return nil, err
	}

	// Get total study sessions
	err = DB.QueryRow(`
		SELECT COUNT(*)
		FROM study_sessions
	`).Scan(&stats.TotalStudySessions)
	if err != nil {
		return nil, err
	}

	// Get total active groups (groups with at least one study session)
	err = DB.QueryRow(`
		SELECT COUNT(DISTINCT group_id)
		FROM study_sessions
	`).Scan(&stats.TotalActiveGroups)
	if err != nil {
		return nil, err
	}

	// Get study streak (consecutive days with at least one study session)
	// Note: This is a simplified version that just counts consecutive days
	err = DB.QueryRow(`
		WITH RECURSIVE dates AS (
			SELECT date(created_at) as study_date
			FROM study_sessions
			GROUP BY date(created_at)
			ORDER BY study_date DESC
			LIMIT 1
		),
		streak(study_date, days) AS (
			SELECT study_date, 1
			FROM dates
			UNION ALL
			SELECT date(study_date, '-1 day'), days + 1
			FROM streak
			WHERE EXISTS (
				SELECT 1
				FROM study_sessions
				WHERE date(created_at) = date(study_date, '-1 day')
			)
		)
		SELECT COUNT(*)
		FROM streak
	`).Scan(&stats.StudyStreakDays)
	if err != nil {
		return nil, err
	}

	return &stats, nil
}
