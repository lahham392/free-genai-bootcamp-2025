package main

import (
	"log"
	"net/http"
	"path/filepath"

	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
	"lang-portal/internal/handlers"
	"lang-portal/internal/services"
)

func main() {
	// Initialize database
	dbPath := filepath.Join(".", "words.db")
	if err := services.InitDB(dbPath); err != nil {
		log.Fatal("Failed to initialize database:", err)
	}
	defer services.DB.Close()

	// Initialize router
	r := gin.Default()

	// CORS middleware
	r.Use(func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Origin, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization")
		if c.Request.Method == http.MethodOptions {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}
		c.Next()
	})

	// Initialize handlers
	h := handlers.NewHandlers(services.DB)

	// API routes
	api := r.Group("/api")
	{
		// Words
		api.GET("/words", h.GetAllWords)
		api.GET("/words/:id", h.GetWord)

		// Groups
		api.GET("/groups", h.GetGroups)
		api.GET("/groups/:id", h.GetGroup)
		api.GET("/groups/:id/words", h.GetGroupWords)
		api.GET("/groups/:id/study_sessions", h.GetGroupStudySessions)

		// Study Activities
		api.GET("/study_activities/:id", h.GetStudyActivity)
		api.GET("/study_activities/:id/study_sessions", h.GetStudyActivitySessions)
		api.POST("/study_activities", h.CreateStudyActivity)

		// Study Sessions
		api.GET("/study_sessions", h.GetStudySessions)
		api.GET("/study_sessions/:id", h.GetStudySession)
		api.GET("/study_sessions/:id/words", h.GetStudySessionWords)
		api.POST("/study_sessions/:id/words/:word_id/review", h.ReviewWord)

		// Reset Endpoints
		api.POST("/reset_history", h.ResetHistory)
		api.POST("/full_reset", h.FullReset)

		// Dashboard
		api.GET("/dashboard/last_study_session", h.GetLastStudySession)
		api.GET("/dashboard/study_progress", h.GetStudyProgress)
		api.GET("/dashboard/quick_stats", h.GetQuickStats)
	}

	// Start server
	log.Println("Server starting on http://localhost:8080")
	if err := r.Run(":8080"); err != nil {
		log.Fatal("Failed to start server:", err)
	}
}
