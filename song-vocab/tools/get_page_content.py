"""Tool for extracting lyrics content from web pages."""

import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional, Dict, List, Tuple
import re
from urllib.parse import urlparse
import time
from fake_useragent import UserAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common lyrics container classes and IDs
LYRICS_SELECTORS = [
    # Classes
    '.lyrics',  # Common on many sites
    '.Lyrics__Container',  # Genius
    '.lyricbox',  # Various sites
    '.songLyricsV14', # AZLyrics
    '.text-lyrics',  # Various sites
    '.SongLyricsV2',  # Various sites
    # IDs
    '#lyrics-content',
    '#lyric-body',
    '#songLyricsDiv',
]

# Elements to remove
UNWANTED_SELECTORS = [
    '.share',  # Share buttons
    '.ads',  # Advertisements
    '.header',  # Headers
    '.footer',  # Footers
    '.comment',  # Comments
    '.social',  # Social media
    'script',  # Scripts
    'style',  # Style tags
    'meta',  # Meta tags
    'iframe',  # iframes
]

class LyricsExtractor:
    def __init__(self):
        """Initialize the LyricsExtractor with common configurations."""
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })

    def _get_domain_specific_extractor(self, domain: str):
        """Get domain-specific extraction method if available."""
        extractors = {
            'genius.com': self._extract_genius,
            'azlyrics.com': self._extract_azlyrics,
            'lyrics.com': self._extract_lyrics_com,
        }
        return extractors.get(domain)

    def _clean_lyrics(self, text: str) -> str:
        """Clean extracted lyrics text."""
        # Split into lines and clean each line
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove [tags] and parentheses
            line = re.sub(r'\[.*?\]', '', line)
            line = re.sub(r'^\([^)]*\)', '', line)
            
            # Clean whitespace
            line = line.strip()
            
            if line:  # Only keep non-empty lines
                cleaned_lines.append(line)
        
        # Join lines with newlines
        return '\n'.join(cleaned_lines)

    def _extract_genius(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract lyrics from Genius.com."""
        logger.info("Attempting to extract from Genius.com")
        logger.info(f"HTML content: {soup.prettify()[:1000]}...")
        
        lyrics_div = soup.find('div', class_='Lyrics__Container')
        if not lyrics_div:
            logger.warning("Could not find Lyrics__Container div")
            return None
        
        # Remove annotations
        for tag in lyrics_div.find_all(class_='AnnotationPopover'):
            tag.decompose()
            
        lyrics = lyrics_div.get_text()
        logger.info(f"Extracted lyrics (first 100 chars): {lyrics[:100]}...")
        return lyrics

    def _extract_azlyrics(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract lyrics from AZLyrics.com."""
        logger.info("Attempting to extract from AZLyrics.com")
        logger.info(f"HTML content: {soup.prettify()[:1000]}...")
        
        lyrics_div = soup.find('div', class_='col-xs-12 col-lg-8 text-center')
        if not lyrics_div:
            logger.warning("Could not find main content div")
            return None
            
        # Find the lyrics div (it's usually unmarked)
        logger.info("Looking for lyrics div...")
        for div in lyrics_div.find_all('div', recursive=False):
            if not div.get('class') and not div.get('id'):
                # Replace <br> tags with newlines
                for br in div.find_all('br'):
                    br.replace_with('\n')
                lyrics = div.get_text()
                logger.info(f"Found lyrics (first 100 chars): {lyrics[:100]}...")
                return lyrics
        
        logger.warning("Could not find lyrics div")
        return None

    def _extract_lyrics_com(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract lyrics from Lyrics.com."""
        logger.info("Attempting to extract from Lyrics.com")
        logger.info(f"HTML content: {soup.prettify()}")
        lyrics_div = soup.find('pre', id='lyric-body-text')
        if lyrics_div:
            logger.info("Found lyrics div on Lyrics.com")
            return lyrics_div.get_text()
        logger.warning("Could not find lyrics div on Lyrics.com")
        return None

    def _extract_generic(self, soup: BeautifulSoup) -> Optional[str]:
        """Generic lyrics extraction for unknown sites."""
        logger.info("Attempting generic extraction")
        # Try common selectors
        for selector in LYRICS_SELECTORS:
            logger.info(f"Trying selector: {selector}")
            element = soup.select_one(selector)
            if element:
                logger.info(f"Found lyrics with selector: {selector}")
                return element.get_text()

        # Fallback: Look for largest text block
        candidates = []
        for tag in soup.find_all(['div', 'pre', 'p']):
            text = tag.get_text().strip()
            if len(text) > 100 and '\n' in text:
                candidates.append((len(text), text))

        if candidates:
            return max(candidates, key=lambda x: x[0])[1]

        return None

    def get_page_content(self, url: str, retries: int = 3) -> Dict[str, str]:
        """
        Extract lyrics content from a webpage.
        
        Args:
            url (str): URL of the lyrics page
            retries (int): Number of retries on failure
            
        Returns:
            Dict[str, str]: Dictionary containing:
                - success: Whether extraction was successful
                - content: Extracted lyrics if successful, error message if not
                - title: Page title if found
        """
        try:
            # Attempt to get the page
            for attempt in range(retries):
                try:
                    # Rotate user agent
                    self.session.headers['User-Agent'] = self.ua.random
                    
                    # Add delay between retries
                    if attempt > 0:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        
                    response = self.session.get(url, timeout=10)
                    logger.info(f"Response status: {response.status_code}")
                    logger.info(f"Response headers: {dict(response.headers)}")
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if attempt == retries - 1:
                        raise
                    logger.warning(f"Retry {attempt + 1}/{retries} failed: {str(e)}")
                    continue

            # Parse domain from response URL for mocking support
            domain = urlparse(response.url).netloc.lower()
            logger.info(f"Detected domain: {domain}")
            if domain.startswith('www.'):
                domain = domain[4:]
            logger.info(f"Normalized domain: {domain}")

            # Parse the page
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unwanted elements
            for selector in UNWANTED_SELECTORS:
                for element in soup.select(selector):
                    element.decompose()

            # Get page title
            title = soup.title.string if soup.title else ''
            
            # Try domain-specific extractor first
            extractor = self._get_domain_specific_extractor(domain)
            if extractor:
                lyrics = extractor(soup)
            else:
                lyrics = self._extract_generic(soup)

            if not lyrics:
                return {
                    'success': False,
                    'content': 'Could not extract lyrics from page',
                    'title': title
                }

            # Clean the lyrics
            lyrics = self._clean_lyrics(lyrics)
            
            if len(lyrics) < 100:  # Probably not real lyrics
                return {
                    'success': False,
                    'content': 'Extracted content too short to be lyrics',
                    'title': title
                }

            return {
                'success': True,
                'content': lyrics,
                'title': title
            }

        except Exception as e:
            logger.error(f"Error extracting content from {url}: {str(e)}")
            return {
                'success': False,
                'content': f"Error extracting content: {str(e)}",
                'title': ''
            }


# Create a helper function to match the import in agent.py
def get_page_content(url: str, retries: int = 3) -> str:
    """
    Helper function to extract lyrics content from a webpage.
    
    Args:
        url (str): URL of the lyrics page
        retries (int): Number of retries on failure
        
    Returns:
        str: Extracted lyrics content or empty string if extraction failed
    """
    extractor = LyricsExtractor()
    result = extractor.get_page_content(url, retries)
    
    if result["success"]:
        return result["content"]
    else:
        return ""
