from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from agent import LyricsAgent
from database import Database

app = FastAPI(title="Song Vocabulary API")
db = Database()

class MessageRequest(BaseModel):
    message_request: str
    artist: Optional[str] = None

class VocabularyWord(BaseModel):
    english: str
    spanish: str = ""
    transliteration: str = ""
    arabic: str = ""

class VocabularyGroup(BaseModel):
    name: str

class VocabularyResponse(BaseModel):
    group: VocabularyGroup
    words: List[VocabularyWord]

class LyricsResponse(BaseModel):
    id: int
    lyrics: str
    vocabulary: VocabularyResponse

class SongResponse(BaseModel):
    id: int
    title: str
    artist: Optional[str] = None
    lyrics: Optional[str] = None
    vocabulary: Optional[VocabularyResponse] = None
@app.post("/api/agent", response_model=LyricsResponse)
async def get_lyrics(request: MessageRequest):
    try:
        agent = LyricsAgent()
        lyrics, vocabulary_data = await agent.process_request(request.message_request)
        
        # Store in database
        song_id = db.add_song(
            title=request.message_request,
            lyrics=lyrics,
            artist=request.artist
        )
        
        # Format vocabulary for database
        vocabulary_words = [{"word": word["english"], "definition": None} for word in vocabulary_data["words"]]
        db.add_vocabulary(song_id, vocabulary_words)
        
        return LyricsResponse(
            id=song_id,
            lyrics=lyrics,
            vocabulary=vocabulary_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/songs", response_model=List[SongResponse])
async def search_songs(q: str = Query(..., description="Search query for song title or artist")):
    try:
        return db.search_songs(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/songs/{song_id}", response_model=SongResponse)
async def get_song(song_id: int):
    try:
        song = db.get_song(song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        
        song['vocabulary'] = db.get_vocabulary_for_song(song_id)
        return song
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
