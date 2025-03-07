import ollama
from typing import Tuple, List, Dict, Optional
import json
import re
from tools.get_page_content import LyricsExtractor, get_page_content
from tools.get_page_content import get_page_content
from tools.extract_vocabulary import extract_vocabulary

def load_prompt(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

SYSTEM_PROMPT = load_prompt('prompts/Lyrics_Agent.md')

class LyricsAgent:
    def __init__(self):
        self.model = "mistral:7b"
        self.max_retries = 3
        self.lyrics_extractor = LyricsExtractor()
        self.max_retries = 3
    
    def _is_valid_lyrics(self, text: str) -> bool:
        """Check if the text appears to be valid song lyrics"""
        if not text or len(text) < 50:  # Too short to be lyrics
            return False
            
        # Check for common lyrics patterns
        lines = text.split('\n')
        if len(lines) < 5:  # Too few lines to be lyrics
            return False
            
        # Check for verse/chorus patterns (repeated lines)
        seen_lines = set()
        repeated_lines = 0
        for line in lines:
            line = line.strip()
            if line in seen_lines:
                repeated_lines += 1
            seen_lines.add(line)
    async def _get_lyrics_from_url(self, url: str) -> Optional[str]:
        """Extract lyrics from a URL with validation"""
        try:
            result = self.lyrics_extractor.get_page_content(url)
            if result["success"] and self._is_valid_lyrics(result["content"]):
                # Clean up the lyrics
                lines = [line.strip() for line in result["content"].split("
") if line.strip()]
                return "
".join(lines)
        except Exception:
            pass
        return None
        except Exception:
            pass
        return None
    
    def _analyze_llm_response(self, response: Dict) -> Dict:
        """Analyze the LLM's response to determine next action"""
        content = response.get('message', {}).get('content', '')
        
        # Extract thought process and action
        thought_match = re.search(r'Thought: (.*?)(?=\nAction:|$)', content, re.DOTALL)
        action_match = re.search(r'Action: (.*?)(?=\nObservation:|$)', content, re.DOTALL)
        
        return {
            'thought': thought_match.group(1).strip() if thought_match else None,
            'action': action_match.group(1).strip() if action_match else None
        }
    async def process_request(self, message: str) -> Tuple[str, Dict]:

    async def process_request(self, message: str) -> Tuple[str, List[str]]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Find lyrics and vocabulary for: {message}"}
        ]
        
        lyrics = None
        search_attempt = 0
        used_urls = set()
        
        while not lyrics and search_attempt < self.max_retries:
            try:
                # Get LLM's next action
                response = ollama.chat(model=self.model, messages=messages)
                analysis = self._analyze_llm_response(response)
                
                # Search for lyrics
                search_query = f"{message} lyrics"
                if search_attempt > 0:
                    search_query += f" site:{'.com' if search_attempt == 1 else '.net'}"
                
                search_results = search_web(search_query)
                
                # Try each search result until we find valid lyrics
                for result in search_results:
                    url = result.get("url")
                    if not url or url in used_urls:
                        continue
                        
                    used_urls.add(url)
                    lyrics = await self._get_lyrics_from_url(url)
                    if lyrics:
                        break
                        
                search_attempt += 1
                
                if not lyrics:
                    # Update conversation with failure
                    messages.append({"role": "assistant", "content": response.get('message', {}).get('content', '')})
                    messages.append({"role": "user", "content": "Could not find valid lyrics. Please try a different approach."})
            
            except Exception as e:
                search_attempt += 1
                messages.append({"role": "user", "content": f"Error occurred: {str(e)}. Please try a different approach."})
        
        if not lyrics:
            raise Exception("Could not find valid lyrics after multiple attempts")
        
        # Extract vocabulary using the model for better context
        vocab_prompt = f"Given these lyrics, identify important vocabulary words that would be educational:\n\n{lyrics}"
        vocab_response = ollama.chat(model=self.model, messages=[{"role": "user", "content": vocab_prompt}])
        
        # Use both the model's suggestions and our vocabulary tool
        tool_vocab_result = extract_vocabulary(lyrics, f"Vocabulary from {message}")
        model_vocabulary = set(re.findall(r'\b\w+\b', vocab_response.get('message', {}).get('content', '')))
        
        # Add model's suggestions to the vocabulary
        existing_words = {word['english'] for word in tool_vocab_result['words']}
        for word in model_vocabulary:
            if len(word) > 2 and word not in existing_words:
                tool_vocab_result['words'].append({
                    'english': word,
                    'spanish': '',
                    'transliteration': '',
                    'arabic': ''
                })
        
        # Sort words by English term
        tool_vocab_result['words'].sort(key=lambda x: x['english'])
        
        return lyrics.strip(), tool_vocab_result
