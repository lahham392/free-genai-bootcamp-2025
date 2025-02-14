package services

import (
	"database/sql"
	"lang-portal/internal/models"
)

type WordService struct{
	db *sql.DB
}

func NewWordService(db *sql.DB) *WordService {
	return &WordService{db: db}
}

func (s *WordService) GetAllWords(page int, itemsPerPage int) ([]models.Word, *PaginationResult, error) {
	var totalItems int
	err := s.db.QueryRow("SELECT COUNT(*) FROM words").Scan(&totalItems)
	if err != nil {
		return nil, nil, err
	}

	totalPages := (totalItems + itemsPerPage - 1) / itemsPerPage
	offset := (page - 1) * itemsPerPage

	rows, err := s.db.Query(`
		SELECT id, spanish, transliteration, arabic
		FROM words
		LIMIT ? OFFSET ?`, itemsPerPage, offset)
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

func (s *WordService) GetWordByID(id int) (*models.Word, error) {
	var word models.Word
	err := s.db.QueryRow(`
		SELECT id, spanish, transliteration, arabic 
		FROM words 
		WHERE id = ?`, id).Scan(&word.ID, &word.Spanish, &word.Transliteration, &word.Arabic)
	if err != nil {
		return nil, err
	}
	return &word, nil
}

func (s *WordService) GetWordStats(wordID int) (int, int, error) {
	var correct, wrong int
	err := s.db.QueryRow(`
		SELECT 
			COUNT(CASE WHEN correct = true THEN 1 END) as correct_count,
			COUNT(CASE WHEN correct = false THEN 1 END) as wrong_count
		FROM word_review_items
		WHERE word_id = ?`, wordID).Scan(&correct, &wrong)
	if err != nil {
		return 0, 0, err
	}
	return correct, wrong, nil
}

func (s *WordService) GetWordGroups(wordID int) ([]models.Group, error) {
	rows, err := s.db.Query(`
		SELECT g.id, g.name
		FROM groups g
		JOIN word_groups wg ON g.id = wg.group_id
		WHERE wg.word_id = ?`, wordID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var groups []models.Group
	for rows.Next() {
		var group models.Group
		if err := rows.Scan(&group.ID, &group.Name); err != nil {
			return nil, err
		}
		groups = append(groups, group)
	}
	return groups, nil
}
