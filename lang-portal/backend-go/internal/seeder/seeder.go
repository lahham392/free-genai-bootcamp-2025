package seeder

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

type Seeder struct {
	db *sql.DB
}

type SeedWord struct {
	Spanish         string `json:"spanish"`
	Transliteration string `json:"transliteration"`
	Arabic          string `json:"arabic"`
}

type SeedGroup struct {
	Name string `json:"name"`
}

type SeedData struct {
	Group SeedGroup  `json:"group"`
	Words []SeedWord `json:"words"`
}

func New(db *sql.DB) *Seeder {
	return &Seeder{db: db}
}

// RunSQLSeeds executes SQL seed files
func (s *Seeder) RunSQLSeeds() error {
	seedFiles, err := os.ReadDir("db/seeds")
	if err != nil {
		return fmt.Errorf("error reading seeds directory: %v", err)
	}

	for _, file := range seedFiles {
		if file.IsDir() || filepath.Ext(file.Name()) != ".sql" {
			continue
		}

		content, err := os.ReadFile(filepath.Join("db/seeds", file.Name()))
		if err != nil {
			return fmt.Errorf("error reading seed file %s: %v", file.Name(), err)
		}

		tx, err := s.db.Begin()
		if err != nil {
			return fmt.Errorf("error starting transaction: %v", err)
		}

		if _, err := tx.Exec(string(content)); err != nil {
			tx.Rollback()
			return fmt.Errorf("error executing seed file %s: %v", file.Name(), err)
		}

		if err := tx.Commit(); err != nil {
			return fmt.Errorf("error committing transaction: %v", err)
		}
	}

	return nil
}

// RunJSONSeeds processes JSON seed files
func (s *Seeder) RunJSONSeeds() error {
	seedFiles, err := os.ReadDir("db/seeds")
	if err != nil {
		return fmt.Errorf("error reading seeds directory: %v", err)
	}

	for _, file := range seedFiles {
		if file.IsDir() || filepath.Ext(file.Name()) != ".json" {
			continue
		}

		content, err := os.ReadFile(filepath.Join("db/seeds", file.Name()))
		if err != nil {
			return fmt.Errorf("error reading seed file %s: %v", file.Name(), err)
		}

		var seedData SeedData
		if err := json.Unmarshal(content, &seedData); err != nil {
			return fmt.Errorf("error parsing seed file %s: %v", file.Name(), err)
		}

		if err := s.processJSONSeed(&seedData); err != nil {
			return fmt.Errorf("error processing seed file %s: %v", file.Name(), err)
		}
	}

	return nil
}

func (s *Seeder) processJSONSeed(data *SeedData) error {
	tx, err := s.db.Begin()
	if err != nil {
		return err
	}
	defer tx.Rollback()

	// Insert group
	result, err := tx.Exec("INSERT INTO groups (name) VALUES (?)", data.Group.Name)
	if err != nil {
		return err
	}

	groupID, err := result.LastInsertId()
	if err != nil {
		return err
	}

	// Insert words and link them to the group
	for _, word := range data.Words {
		result, err := tx.Exec(
			"INSERT INTO words (spanish, transliteration, arabic) VALUES (?, ?, ?)",
			word.Spanish, word.Transliteration, word.Arabic,
		)
		if err != nil {
			return err
		}

		wordID, err := result.LastInsertId()
		if err != nil {
			return err
		}

		_, err = tx.Exec(
			"INSERT INTO word_groups (word_id, group_id) VALUES (?, ?)",
			wordID, groupID,
		)
		if err != nil {
			return err
		}
	}

	return tx.Commit()
}
