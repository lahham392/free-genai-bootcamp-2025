# Backedn Server Technical Specs

## Business Goal: 
A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary that can be learned
- Act as a  Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps

## Technical Requirements

- The backend will be built using Go
- The database will be SQLite3
- The API will be built using Gin
- The API will always return JSON
- There will be no authentication or authorization
- Everything treated as a single user

## Database Schema

We have the following tables in the database:
- words - stored the vocabulary words
  - id integer
  - spanish string
  - transliteration string
  - arabic string
  - parts json

- word_groups - joint table for words and groups many to many relationship
    - id integer
    - word_id integer
    - group_id integer

- groups - thematic groups of words
    - id integer
    - name string

- study_sessions - records of study sessions grouping word_review_items
    - id integer
    - created_at datetime
    - group_id integer
    - study_activity string



- study_activities - a specific study activity, like a quiz or a flashcard session. linking a study_sessions to group
    - id integer
    - study_session_id integer
    - group_id integer
    - created_at datetime

- word_review_items - a record of word practice, determining if the word was correct or not
    - word_id integer
    - study_session_id integer
    - correct boolean
    - created_at datetime

## API Endpoints


### GET /api/words/:id - returns a single word
#### JSON Response
```json
{
  "spanish": "hola",
  "transliteration": "هولا",
  "arabic": "مرحبا",
  "stats": {
    "correct_count": 15,
    "wrong_count": 3
  },
  "groups": [
    {
      "id": 1,
      "name": "Greetings"
    }
  ]
}
```

### GET /api/groups - returns all groups
pagination with 100 items per page
#### API Response
```json
{
  "items": [
    {
      "id": 1,
      "name": "Greetings",
      "word_count": 15
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 1000,
    "items_per_page": 100
  }
}
```

### GET /api/groups/:id - returns a single group
#### API Response
```json
{
  "id": 1,
  "name": "Greetings",
  "stats": {
    "total_words_count": 15,
  },
}
```

### GET /api/groups/:id/words - returns all words in a group
#### API Response
```json
{
  "items": [
    {
      "spanish": "hola",
      "transliteration": "هولا",
      "arabic": "مرحبا",
      "correct_count": 15,
      "wrong_count": 3
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 1000,
    "items_per_page": 100
  }
}
```


### GET /api/dashboard/last_study_session
Returns information about the most recent study session.
#### JSON Response
```json
{
  "id": 1,
  "created_at": "2024-02-14T12:00:00Z",
  "group_id": 1,
  "group_name": "Greetings",
  "study_activity_id": "flashcards",
  "word_count": 15,
  "correct_count": 12,
  "accuracy": 80
}
```

### GET /api/dashboard/study_progress
Returns study progress statistics for the dashboard.
#### JSON Response
```json
{
  "total_words_studied": 10,
  "total_available_words": 500,
}
```

### GET /api/dashboard/quick_stats
Returns quick overview statistics for the dashboard.
#### JSON Response
```json
{
  "success_rate": 63,
  "total_study_sessions": 5,
  "total_active_groups": 3,
  "study_streak_days": 3,
}
```


### GET /api/study_activities/:id
#### JSON Response
```json
{
    "id": 1,
    "name": "Flashcards",
    "description": "Practice vocabulary with digital flashcards",
    "thumbnail_url": "/thumbnails/flashcards.png"
}
```

### GET /api/study_activities/:id/study_sessions
pagination with 100 items per page
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Greetings",
      "group_name": "Greetings",
      "start_time": "2024-02-14T12:00:00Z",
      "end_time": "2024-02-14T12:30:00Z",
      "review_items_count": 15
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_items": 5,
    "items_per_page": 100
  }
}
```

### POST /api/study_activities
### Request Parameters 
- group_id
- study_activity_id

#### JSON Response

```json
{
  "id": 1,
  "group_id": 1
}
```

### GET /api/words
pagination with 100 items per page
#### JSON Response
```json
{
  "items": [
    {
      "spanish": "hola",
      "transliteration": "هولا",
      "arabic": "مرحبا",
      "correct_count": 15,
      "wrong_count": 3
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 1000,
    "items_per_page": 100
  }
}
```

### GET /api/groups/:id/study_sessions
#### JSON Response
```JSON
{
  "items": [
    {
      "id": 1,
      "activity_name": "Greetings",
      "group_name": "Greetings",
      "start_time": "2024-02-14T12:00:00Z",
      "end_time": "2024-02-14T12:30:00Z",
      "review_items_count": 15
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Greetings",
      "group_name": "Greetings",
      "start_time": "2024-02-14T12:00:00Z",
      "end_time": "2024-02-14T12:30:00Z",
      "review_items_count": 15
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions/:id
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Greetings",
      "group_name": "Greetings",
      "start_time": "2024-02-14T12:00:00Z",
      "end_time": "2024-02-14T12:30:00Z",
      "review_items_count": 15
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "items_per_page": 100
  }
}
```

### GET /api/study_sessions/:id/words
#### JSON Response
```json
{
  "items": [
    {
      "id": 1,
      "activity_name": "Greetings",
      "group_name": "Greetings",
      "start_time": "2024-02-14T12:00:00Z",
      "end_time": "2024-02-14T12:30:00Z",
      "review_items_count": 15
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "items_per_page": 100
  }
}
```

### POST /api/reset_history
#### JSON Response
```json
{
  "success": true,
  "message": "Study history has been reset"
}
```

### POST /api/full_reset
#### JSON Response
```json
{
  "success": true,
  "message": "All data has been reset",
}
```

### POST /api/study_sessions/:id/words/:word_id/review
#### Request Parameters
- id (study_session_id) integer
- word_id integer
- correct boolean
#### Request Payload
```json
{
  "correct": true
}
```
#### JSON Response
```json
{
  "success": true,
  "study_session_id": 1,
  "word_id": 1,
  "correct": true,
  "created_at": "2024-02-14T12:00:00Z"
}
```

## Mage Tasks
Mage is task runner for Go.
