package models

import (
	"time"
)

type Word struct {
	ID              int    `json:"id"`
	Spanish         string `json:"spanish"`
	Transliteration string `json:"transliteration"`
	Arabic          string `json:"arabic"`
}

type Group struct {
	ID        int    `json:"id"`
	Name      string `json:"name"`
	WordCount int    `json:"word_count,omitempty"`
}

type PaginationResult struct {
	CurrentPage  int `json:"current_page"`
	TotalPages   int `json:"total_pages"`
	TotalItems   int `json:"total_items"`
	ItemsPerPage int `json:"items_per_page"`
}

type StudySession struct {
	ID              int       `json:"id"`
	ActivityName    string    `json:"activity_name"`
	GroupName       string    `json:"group_name"`
	StartTime       time.Time `json:"start_time"`
	EndTime         time.Time `json:"end_time"`
	ReviewItemCount int       `json:"review_items_count"`
	CreatedAt       time.Time `json:"created_at"`
	GroupID         int       `json:"group_id"`
	Activity        string    `json:"study_activity"`
}

type WordGroup struct {
	ID      int `json:"id"`
	WordID  int `json:"word_id"`
	GroupID int `json:"group_id"`
}

type StudyActivity struct {
	ID             int       `json:"id"`
	StudySessionID int       `json:"study_session_id"`
	GroupID        int       `json:"group_id"`
	CreatedAt      time.Time `json:"created_at"`
}

type WordReviewItem struct {
	WordID         int       `json:"word_id"`
	StudySessionID int       `json:"study_session_id"`
	Correct        bool      `json:"correct"`
	CreatedAt      time.Time `json:"created_at"`
}
