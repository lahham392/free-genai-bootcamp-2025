"""Test suite for lyrics search and extraction tools."""

import sys
import os
import unittest
from pathlib import Path

# Add the parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from tools.search_web import search_web
from tools.get_page_content import LyricsExtractor

class TestLyricsTools(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = LyricsExtractor()
    
    def test_lyrics_extraction(self):
        """Test lyrics extraction from a known lyrics page."""
        print("\nTesting lyrics extraction...")
        
        # Test with a known AZLyrics page
        url = "https://www.azlyrics.com/lyrics/imaginedragons/believer.html"
        print(f"Extracting from: {url}")
        
        result = self.extractor.get_page_content(url)
        
        print("\nExtraction result:")
        print(f"Success: {result['success']}")
        if result['success']:
            print(f"Title: {result['title']}")
            print(f"First 100 chars: {result['content'][:100]}...")
        
        # Verify we got meaningful lyrics
        self.assertTrue(result['success'], "Should successfully extract lyrics")
        self.assertTrue(len(result['content']) > 100, "Lyrics should be substantial")
        self.assertTrue('\n' in result['content'], "Lyrics should have line breaks")
        self.assertIn('believer', result['title'].lower(), "Title should match song")

if __name__ == '__main__':
    unittest.main(verbosity=2)
