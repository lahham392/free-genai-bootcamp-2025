//go:build mage
package main

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"

	"github.com/magefile/mage/sh"
	_ "github.com/mattn/go-sqlite3"
	"lang-portal/internal/seeder"
)

// Init initializes the project
func Init() error {
	if err := sh.Run("go", "mod", "tidy"); err != nil {
		return err
	}
	return nil
}

// Migrate runs database migrations
func Migrate() error {
	db, err := sql.Open("sqlite3", "words.db")
	if err != nil {
		return err
	}
	defer db.Close()

	migrationFiles, err := os.ReadDir("db/migrations")
	if err != nil {
		return err
	}

	for _, file := range migrationFiles {
		if file.IsDir() {
			continue
		}

		content, err := os.ReadFile(filepath.Join("db/migrations", file.Name()))
		if err != nil {
			return err
		}

		if _, err := db.Exec(string(content)); err != nil {
			return fmt.Errorf("error executing migration %s: %v", file.Name(), err)
		}
	}

	return nil
}

// Seed runs both SQL and JSON seeds
func Seed() error {
	db, err := sql.Open("sqlite3", "words.db")
	if err != nil {
		return err
	}
	defer db.Close()

	s := seeder.New(db)

	// Run SQL seeds first
	if err := s.RunSQLSeeds(); err != nil {
		return fmt.Errorf("error running SQL seeds: %v", err)
	}

	// Then run JSON seeds
	if err := s.RunJSONSeeds(); err != nil {
		return fmt.Errorf("error running JSON seeds: %v", err)
	}

	return nil
}

// Setup runs migrations and seeds
func Setup() error {
	if err := Migrate(); err != nil {
		return err
	}
	if err := Seed(); err != nil {
		return err
	}
	return nil
}

// Run starts the server
func Run() error {
	return sh.Run("go", "run", "cmd/server/main.go")
}
