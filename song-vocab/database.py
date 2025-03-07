import sqlite3
from typing import List, Dict, Optional
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "song_vocab.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        """Initialize the database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create songs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT,
                    lyrics TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create vocabulary table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vocabulary (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    song_id INTEGER,
                    word TEXT NOT NULL,
                    definition TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (song_id) REFERENCES songs (id)
                )
            """)
            
            conn.commit()

    def add_song(self, title: str, lyrics: str, artist: Optional[str] = None) -> int:
        """Add a new song to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO songs (title, artist, lyrics) VALUES (?, ?, ?)",
                (title, artist, lyrics)
            )
            conn.commit()
            return cursor.lastrowid

    def add_vocabulary(self, song_id: int, words: List[Dict[str, str]]):
        """Add vocabulary words for a song"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for word_data in words:
                cursor.execute(
                    "INSERT INTO vocabulary (song_id, word, definition) VALUES (?, ?, ?)",
                    (song_id, word_data['word'], word_data.get('definition'))
                )
            conn.commit()

    def get_song(self, song_id: int) -> Optional[Dict]:
        """Get a song by its ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, artist, lyrics FROM songs WHERE id = ?", (song_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'artist': row[2],
                    'lyrics': row[3]
                }
            return None
    def get_vocabulary_for_song(self, song_id: int) -> Dict:
        """Get all vocabulary words for a song in the format expected by VocabularyResponse"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT word, definition FROM vocabulary WHERE song_id = ?",
                (song_id,)
            )
            words = []
            for row in cursor.fetchall():
                words.append({
                    "english": row[0],
                    "spanish": "",
                    "transliteration": "",
                    "arabic": ""
                })
            
            # Get song title for group name
            cursor.execute("SELECT title FROM songs WHERE id = ?", (song_id,))
            title = cursor.fetchone()[0]
            
            return {
                "group": {"name": f"Vocabulary from {title}"},
                "words": words
            }
            return [{'word': row[0], 'definition': row[1]} for row in cursor.fetchall()]

    def search_songs(self, query: str) -> List[Dict]:
        """Search for songs by title or artist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, artist 
                FROM songs 
                WHERE title LIKE ? OR artist LIKE ?
                """,
                (f"%{query}%", f"%{query}%")
            )
            return [
                {'id': row[0], 'title': row[1], 'artist': row[2]}
                for row in cursor.fetchall()
            ]
