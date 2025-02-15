# Language Learning Backend Application

This document explains the backend server for our language learning application, designed for beginners in programming and Go.

## 1. Overview
This is a web application that helps people learn languages (Spanish and Arabic). It's built using Go (also called Golang) for the backend server. Think of it as the "brain" behind a language learning app.

## 2. Technologies Used

### 2.1 Main Technologies
- **Go (Golang)**: The main programming language
- **Gin**: A web framework that helps create web APIs easily
- **SQLite**: A simple database that stores all our data in a single file
- **Mage**: A tool that helps automate tasks like setting up the database

### 2.2 Database
The database (SQLite) stores:
- Words in different languages
- Groups of related words (like "Greetings", "Numbers", etc.)
- Study sessions (when users practice)
- Study activities (what users did during practice)

## 3. Project Structure
```
backend-go/
├── cmd/
│   └── server/           # Main application entry point
├── internal/
│   ├── handlers/         # Code that handles web requests
│   └── services/         # Business logic
├── db/
│   ├── migrations/       # Database structure setup
│   └── seeds/           # Initial data for the database
```

## 4. How It Works (Step by Step)

### 4.1 Starting the Server
When you start the application:
1. The server starts (in `main.go`)
2. It connects to the database
3. Sets up all the routes (URLs) that users can access
4. Starts listening for requests

### 4.2 API Endpoints (URLs)
The application provides several URLs that users can access:

1. **Words**
   - `GET /api/words`: Get all vocabulary words
   ```json
   {
     "items": [
       {
         "id": 1,
         "spanish": "hola",
         "transliteration": "هولا",
         "arabic": "مرحبا"
       }
     ]
   }
   ```

2. **Groups**
   - `GET /api/groups`: Get all word groups (like "Greetings", "Numbers")
   ```json
   {
     "items": [
       {
         "id": 1,
         "name": "Greetings",
         "word_count": 3
       }
     ]
   }
   ```

3. **Study Sessions**
   - `POST /api/study_activities`: Start a new study session
   - `GET /api/study_sessions`: See all study sessions
   - `POST /api/study_sessions/1/words/1/review`: Record when a user practices a word

### 4.3 Database Tables
The database has several tables:

1. **words**: Stores vocabulary
   - id
   - spanish (word in Spanish)
   - arabic (word in Arabic)
   - transliteration (Arabic pronunciation in Latin letters)

2. **groups**: Categories of words
   - id
   - name (like "Greetings", "Numbers")

3. **study_sessions**: Records of practice sessions
   - id
   - created_at (when the session started)
   - group_id (which word group was practiced)
   - study_activity (what type of practice, like "Flashcards")

4. **study_activities**: Details of what happened in each session
   - id
   - study_session_id (which session this belongs to)
   - created_at (when this activity happened)

## 5. Code Components Explained

### 5.1 Handlers (handlers.go)
Handlers are like receptionists - they:
1. Receive requests from users
2. Check if the request is valid
3. Pass the request to the right service
4. Send back the response

Example:
```go
// This function handles getting all words
func (h *Handler) GetWords(c *gin.Context) {
    // Get page number from request
    page := getPage(c)
    
    // Ask the service to get the words
    words, pagination, err := h.wordService.GetWords(page, itemsPerPage)
    
    // If there's an error, return it
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    
    // Return the words to the user
    c.JSON(http.StatusOK, gin.H{
        "items":      words,
        "pagination": pagination,
    })
}
```

### 5.2 Services (study_service.go, word_service.go)
Services contain the business logic - they:
1. Handle the actual work
2. Talk to the database
3. Process data
4. Make sure everything follows the rules

Example:
```go
// This function gets words from the database
func (s *WordService) GetWords(page, itemsPerPage int) ([]Word, *PaginationResult, error) {
    // Calculate where to start in the database
    offset := (page - 1) * itemsPerPage
    
    // Get words from database
    rows, err := s.db.Query(`
        SELECT id, spanish, transliteration, arabic
        FROM words
        LIMIT ? OFFSET ?
    `, itemsPerPage, offset)
    
    // Process the results
    var words []Word
    for rows.Next() {
        var word Word
        rows.Scan(&word.ID, &word.Spanish, &word.Transliteration, &word.Arabic)
        words = append(words, word)
    }
    
    return words, pagination, nil
}
```

## 6. How It All Works Together

When someone uses the application:

1. **User makes a request** (like getting all words)
   ```
   GET http://localhost:8080/api/words
   ```

2. **Gin (web framework) receives the request**
   - Checks if the URL is valid
   - Finds the right handler

3. **Handler processes the request**
   - Gets any parameters (like page number)
   - Calls the appropriate service

4. **Service does the work**
   - Talks to the database
   - Gets or updates data
   - Applies any business rules

5. **Response goes back to user**
   - Data is converted to JSON
   - Sent back to the user's browser

## 7. Running the Application

1. Make sure you have Go installed
2. Clone the repository
3. Navigate to the backend-go folder
4. Run the following commands:
   ```bash
   go mod download  # Download dependencies
   go run cmd/server/main.go  # Start the server
   ```
5. The server will start at `http://localhost:8080`

## 8. Testing the API

You can test the API using curl commands:

```bash
# Get all words
curl http://localhost:8080/api/words

# Get all groups
curl http://localhost:8080/api/groups

# Start a study session
curl -X POST http://localhost:8080/api/study_activities -H "Content-Type: application/json" -d '{"group_id": 1, "activity_name": "Flashcards"}'
```

## 9. Need Help?

If you need help understanding any part of the code or want to make changes:
1. Check the comments in the code
2. Look at the test files for examples
3. Refer to this README for overall structure
4. Ask for help in the project's issues section
