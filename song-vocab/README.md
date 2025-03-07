# Song Vocabulary API

A FastAPI application that finds song lyrics and extracts vocabulary using an AI agent with tool use capabilities.

## Features

- Search for song lyrics on the internet
- Extract vocabulary from lyrics
- AI-powered agent using Mistral 7B
- RESTful API endpoints

## Requirements

- Python 3.8+
- FastAPI
- Ollama (with Mistral 7B model)
- SQLite3
- Additional dependencies in requirements.txt

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure Ollama is installed and the Mistral 7B model is available.

## Usage

1. Start the FastAPI server:
```bash
python main.py
```

2. The API will be available at http://localhost:8000

3. Use the POST /api/agent endpoint to search for lyrics and get vocabulary:
```bash
curl -X POST "http://localhost:8000/api/agent" \
     -H "Content-Type: application/json" \
     -d '{"message_request": "Shape of You by Ed Sheeran"}'
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
