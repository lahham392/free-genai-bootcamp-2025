package handlers

import (
	"database/sql"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"lang-portal/internal/services"
)

type Handlers struct {
	wordService      *services.WordService
	groupService     *services.GroupService
	dashboardService *services.DashboardService
	studyService     *services.StudyService
}

func NewHandlers(db *sql.DB) *Handlers {
	return &Handlers{
		wordService:      services.NewWordService(db),
		groupService:     services.NewGroupService(db),
		dashboardService: services.NewDashboardService(db),
		studyService:     services.NewStudyService(db),
	}
}

func (h *Handlers) GetWord(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	word, err := h.wordService.GetWordByID(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	correct, wrong, err := h.wordService.GetWordStats(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	groups, err := h.wordService.GetWordGroups(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"spanish":         word.Spanish,
		"transliteration": word.Transliteration,
		"arabic":         word.Arabic,
		"stats": gin.H{
			"correct_count": correct,
			"wrong_count":   wrong,
		},
		"groups": groups,
	})
}

func (h *Handlers) GetGroups(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	groups, pagination, err := h.groupService.GetGroups(page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      groups,
		"pagination": pagination,
	})
}

func (h *Handlers) GetGroup(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	group, err := h.groupService.GetGroupByID(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, group)
}

func (h *Handlers) GetGroupWords(c *gin.Context) {
	groupID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	words, pagination, err := h.groupService.GetGroupWords(groupID, page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      words,
		"pagination": pagination,
	})
}

func (h *Handlers) GetLastStudySession(c *gin.Context) {
	session, err := h.dashboardService.GetLastStudySession()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, session)
}

func (h *Handlers) GetStudyProgress(c *gin.Context) {
	progress, err := h.dashboardService.GetStudyProgress()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, progress)
}

func (h *Handlers) GetQuickStats(c *gin.Context) {
	stats, err := h.dashboardService.GetQuickStats()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, stats)
}

func (h *Handlers) GetAllWords(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	words, pagination, err := h.wordService.GetAllWords(page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      words,
		"pagination": pagination,
	})
}

func (h *Handlers) GetGroupStudySessions(c *gin.Context) {
	groupID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid group ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	sessions, pagination, err := h.groupService.GetGroupStudySessions(groupID, page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      sessions,
		"pagination": pagination,
	})
}

func (h *Handlers) GetStudyActivity(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid activity ID"})
		return
	}

	activity, err := h.studyService.GetStudyActivity(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, activity)
}

func (h *Handlers) GetStudyActivitySessions(c *gin.Context) {
	activityID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid activity ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	sessions, pagination, err := h.studyService.GetStudyActivitySessions(activityID, page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      sessions,
		"pagination": pagination,
	})
}

func (h *Handlers) GetStudySessions(c *gin.Context) {
	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	sessions, pagination, err := h.studyService.GetStudySessions(page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      sessions,
		"pagination": pagination,
	})
}

func (h *Handlers) GetStudySession(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid session ID"})
		return
	}

	session, err := h.studyService.GetStudySession(id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, session)
}

func (h *Handlers) GetStudySessionWords(c *gin.Context) {
	sessionID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid session ID"})
		return
	}

	page, _ := strconv.Atoi(c.DefaultQuery("page", "1"))
	itemsPerPage := 100

	words, pagination, err := h.studyService.GetStudySessionWords(sessionID, page, itemsPerPage)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"items":      words,
		"pagination": pagination,
	})
}

func (h *Handlers) CreateStudyActivity(c *gin.Context) {
	var req struct {
		GroupID      int    `json:"group_id"`
		ActivityName string `json:"activity_name"`
	}

	if err := c.BindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload"})
		return
	}

	activityID, err := h.studyService.CreateStudyActivity(req.GroupID, req.ActivityName)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, gin.H{
		"id":       activityID,
		"group_id": req.GroupID,
	})
}

func (h *Handlers) ResetHistory(c *gin.Context) {
	if err := h.studyService.ResetHistory(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "Study history has been reset",
	})
}

func (h *Handlers) FullReset(c *gin.Context) {
	if err := h.studyService.FullReset(); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"success": true,
		"message": "All data has been reset",
	})
}

func (h *Handlers) ReviewWord(c *gin.Context) {
	sessionID, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid session ID"})
		return
	}

	wordID, err := strconv.Atoi(c.Param("word_id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid word ID"})
		return
	}

	var req struct {
		Correct bool `json:"correct"`
	}

	if err := c.BindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload"})
		return
	}

	review, err := h.studyService.ReviewWord(sessionID, wordID, req.Correct)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, review)
}
