"""This tool uses DuckDuckGo to search the internet for song lyrics pages."""

from duckduckgo_search import DDGS
from typing import List, Dict, Optional
import re
import logging
import time
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of trusted lyrics domains
TRUSTED_DOMAINS = {
    'genius.com',
    'azlyrics.com',
    'lyrics.com',
    'musixmatch.com',
    'songlyrics.com',
    'metrolyrics.com',
    'lyricsfreak.com',
    'lyricfinder.org',
}

def is_lyrics_url(url: str) -> bool:
    """
    Check if a URL is likely to be a lyrics page
    
    Args:
        url (str): URL to check
        
    Returns:
        bool: True if the URL is likely a lyrics page
    """
    try:
        # Parse the URL
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
            
        # Check if domain is trusted
        if domain in TRUSTED_DOMAINS:
            return True
            
        # Check URL path for lyrics indicators
        path = parsed.path.lower()
        lyrics_indicators = ['lyrics', 'text', 'letras', 'paroles']
        return any(indicator in path for indicator in lyrics_indicators)
        
    except Exception as e:
        logger.warning(f"Error checking URL {url}: {str(e)}")
        return False

def clean_snippet(snippet: str) -> str:
    """
    Clean and format the search result snippet
    
    Args:
        snippet (str): Raw snippet from search results
        
    Returns:
        str: Cleaned snippet
    """
    # Remove extra whitespace
    snippet = ' '.join(snippet.split())
    
    # Remove HTML tags
    snippet = re.sub(r'<[^>]+>', '', snippet)
    
    # Truncate if too long
    max_length = 200
    if len(snippet) > max_length:
        snippet = snippet[:max_length] + '...'
    
    return snippet

def search_web(query: str, max_results: int = 10, max_retries: int = 3) -> List[Dict[str, str]]:
    """
    Search the web for lyrics using DuckDuckGo with retries and rate limiting
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        max_retries (int): Maximum number of retry attempts
        
    Returns:
        List[Dict[str, str]]: List of search results, each containing:
            - url: Page URL
            - title: Page title
            - snippet: Brief description/preview
    """
    # Add 'lyrics' to the query if not present
    if 'lyrics' not in query.lower():
        query = f"{query} lyrics"
    
    for attempt in range(max_retries):
        try:
            results = []
            with DDGS() as ddgs:
                # Search with region set to 'wt-wt' (no region) for broader results
                for r in ddgs.text(query, region='wt-wt', safesearch='off'):
                    if len(results) >= max_results:
                        break
                        
                    url = r.get('link')
                    if not url or not is_lyrics_url(url):
                        continue
                        
                    results.append({
                        'url': url,
                        'title': r.get('title', ''),
                        'snippet': clean_snippet(r.get('body', ''))
                    })
            
            logger.info(f"Found {len(results)} lyrics results for query: {query}")
            return results
            
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                # Exponential backoff
                time.sleep(2 ** attempt)
                continue
            else:
                logger.error(f"All {max_retries} attempts failed for query: {query}")
                return []