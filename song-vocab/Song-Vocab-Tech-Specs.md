# Tech Specs

## Business Goals
We want to create a program that will find lyrics off the internet for a target song in a specific langugae and produce vocabulary to be imported into our database.

## Technical Requirements
- FastAPI
- Python
- Ollama via the Ollama Python SDK
  - Mestral 7B
- SQLite3 (for database)
- Instructor (for structure json output)
- duckduckgo-search (to search for lyrics)

## API Endpoints

### GetLyrics POST /api/agent

### Behavior
This endpoint goes to our agent which is uses the reAct framework so it can go to the internet, find multiple possible version of lyrics. and then extract out the correct lyrics and format the lyrics into vocabulary.

Tools availble:
- tools/extract_vocabulary.py
- tools/get_page_count.py
- tools/search_web.py

#### JSON Request Parameters
- `message_request` (str) (required) - a string that describes the song and/or artist to get lyrics for a song from the internet

#### JSON Response Parameters
- `lyrics` (str) - the lyrics of the song
- `vocabulary` (list) - a list of vocabulary words found in the lyrics

