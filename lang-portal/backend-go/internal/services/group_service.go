package services

import (
	"database/sql"
	"lang-portal/internal/models"
)

type GroupService struct{
	db *sql.DB
}

func NewGroupService(db *sql.DB) *GroupService {
	return &GroupService{db: db}
}

type PaginationResult struct {
	CurrentPage   int `json:"current_page"`
	TotalPages    int `json:"total_pages"`
	TotalItems    int `json:"total_items"`
	ItemsPerPage  int `json:"items_per_page"`
}

func (s *GroupService) GetGroups(page int, itemsPerPage int) ([]models.Group, *PaginationResult, error) {
	// Get total count
	var totalItems int
	err := s.db.QueryRow("SELECT COUNT(*) FROM groups").Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage

	offset := (page - 1) * itemsPerPage
	rows, err := s.db.Query(`
		SELECT g.id, g.name, COUNT(wg.word_id) as word_count
		FROM groups g
		LEFT JOIN word_groups wg ON g.id = wg.group_id
		GROUP BY g.id
		LIMIT ? OFFSET ?`, itemsPerPage, offset)
	if err != nil {
		return nil, nil, err
	}
	defer rows.Close()

	var groups []models.Group
	for rows.Next() {
		var group models.Group
		if err := rows.Scan(&group.ID, &group.Name, &group.WordCount); err != nil {
			return nil, nil, err
		}
		groups = append(groups, group)
	}

	pagination := &PaginationResult{
		CurrentPage:   page,
		TotalPages:    totalPages,
		TotalItems:    totalItems,
		ItemsPerPage:  itemsPerPage,
	}

	return groups, pagination, nil
}

func (s *GroupService) GetGroupByID(id int) (*models.Group, error) {
	var group models.Group
	err := s.db.QueryRow(`
		SELECT g.id, g.name, COUNT(wg.word_id) as word_count
		FROM groups g
		LEFT JOIN word_groups wg ON g.id = wg.group_id
		WHERE g.id = ?
		GROUP BY g.id`, id).Scan(&group.ID, &group.Name, &group.WordCount)
	if err != nil {
		return nil, err
	}
	return &group, nil
}

func (s *GroupService) GetGroupStudySessions(groupID, page, itemsPerPage int) ([]StudySession, *PaginationResult, error) {
	var totalItems int
	err := s.db.QueryRow(`
		SELECT COUNT(*)
		FROM study_sessions ss
		WHERE ss.group_id = ?`, groupID).Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage
	offset := (page - 1) * itemsPerPage

	rows, err := s.db.Query(`
		SELECT 
			ss.id,
			sa.name as activity_name,
			g.name as group_name,
			ss.created_at as start_time,
			ss.created_at as end_time,
			COUNT(wri.word_id) as review_items_count
		FROM study_sessions ss
		JOIN study_activities sa ON ss.study_activity_id = sa.id
		JOIN groups g ON ss.group_id = g.id
		LEFT JOIN word_review_items wri ON ss.id = wri.study_session_id
		WHERE ss.group_id = ?
		GROUP BY ss.id
		ORDER BY ss.created_at DESC
		LIMIT ? OFFSET ?`, groupID, itemsPerPage, offset)
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

func (s *GroupService) GetGroupWords(groupID, page, itemsPerPage int) ([]models.Word, *PaginationResult, error) {
	// Get total count
	var totalItems int
	err := s.db.QueryRow(`
		SELECT COUNT(*) 
		FROM words w
		JOIN word_groups wg ON w.id = wg.word_id
		WHERE wg.group_id = ?`, groupID).Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage

	offset := (page - 1) * itemsPerPage
	rows, err := s.db.Query(`
		SELECT w.id, w.spanish, w.transliteration, w.arabic
		FROM words w
		JOIN word_groups wg ON w.id = wg.word_id
		WHERE wg.group_id = ?
		LIMIT ? OFFSET ?`, groupID, itemsPerPage, offset)
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
		CurrentPage:   page,
		TotalPages:    totalPages,
		TotalItems:    totalItems,
		ItemsPerPage:  itemsPerPage,
	}

	return words, pagination, nil
}
