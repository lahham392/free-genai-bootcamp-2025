"""This tool takes a body of text and extracts all vocabulary from it using NLP techniques."""

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import words
from nltk.tag import pos_tag
from typing import List, Set
import string
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/words')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('punkt')
    nltk.download('words')
    nltk.download('averaged_perceptron_tagger')

# Initialize English word set
english_words = set(words.words())

# Add common contractions to English words
common_contractions = {
    "i'm", "you're", "he's", "she's", "it's", "we're", "they're",
    "i've", "you've", "we've", "they've",
    "i'll", "you'll", "he'll", "she'll", "it'll", "we'll", "they'll",
    "i'd", "you'd", "he'd", "she'd", "it'd", "we'd", "they'd",
    "isn't", "aren't", "wasn't", "weren't",
    "don't", "doesn't", "didn't",
    "can't", "couldn't", "won't", "wouldn't",
    "that's", "what's", "who's", "where's", "when's", "why's", "how's"
}
english_words.update(common_contractions)

# Add common short words that are valid
short_words = {'a', 'i', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 
               'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us',
               'we', 'am', 'the', 'and', 'but', 'for', 'not', 'you', 'she', 'they'}
english_words.update(short_words)

def load_prompt(file_path: str) -> str:
    """Load the system prompt from file"""
    with open(file_path, 'r') as f:
        return f.read()

# Load the system prompt
SYSTEM_PROMPT = load_prompt('prompts/Vocabulary_Extractor.md')

def is_valid_word(word: str) -> bool:
    """
    Check if a word is valid based on the criteria in the prompt
    
    Args:
        word (str): The word to check
        
    Returns:
        bool: True if the word is valid, False otherwise
    """
    word = word.lower()
    
    # Remove any non-alphabetic characters for checking
    clean_word = ''.join(c for c in word if c.isalpha())
    
    # Skip empty strings or single characters (except 'a' and 'i')
    if not clean_word or (len(clean_word) == 1 and clean_word not in {'a', 'i'}):
        return False
    
    # Check if it's in our expanded English word set
    return clean_word in english_words

def clean_text(text: str) -> str:
    """
    Clean text by removing song structure notes while preserving contractions
    
    Args:
        text (str): The text to clean
        
    Returns:
        str: Cleaned text
    """
    # Remove square brackets and their contents (often song structure notes)
    text = re.sub(r'\[.*?\]', '', text)
    
    # Remove parentheses and their contents (often song notes or alternate lyrics)
    text = re.sub(r'\(.*?\)', '', text)
    
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    
    return text.strip()

from dataclasses import dataclass
from typing import Dict, Any, Set
import json

@dataclass
class VocabularyWord:
    english: str
    spanish: str = ""
    transliteration: str = ""
    arabic: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {
            "english": self.english,
            "spanish": self.spanish,
            "transliteration": self.transliteration,
            "arabic": self.arabic
        }

def extract_words_from_text(text: str) -> Set[str]:
    """
    Extract all valid words from the text
    
    Args:
        text (str): The text to process
        
    Returns:
        Set[str]: Set of valid words
    """
    # Clean the text while preserving contractions
    cleaned_text = clean_text(text)
    
    # Tokenize the text
    tokens = word_tokenize(cleaned_text)
    
    # Extract valid words
    words = set()
    for token in tokens:
        # Skip if token contains numbers
        if any(c.isdigit() for c in token):
            continue
            
        # Check if it's a valid word
        if is_valid_word(token):
            words.add(token.lower())
    
    return words

def extract_vocabulary(text: str, group_name: str = "Song Vocabulary") -> Dict[str, Any]:
    """
    Extract ALL vocabulary words from song lyrics and format them according to the required JSON structure
    
    Args:
        text (str): The lyrics text to process
        group_name (str): Name of the vocabulary group
        
    Returns:
        Dict[str, Any]: Dictionary in the format:
        {
            "group": {"name": "group_name"},
            "words": [{"english": "word1", "spanish": "", ...}, ...]
        }
    """
    # Extract all valid words
    vocabulary = extract_words_from_text(text)
    
    # Create vocabulary words list
    vocab_words = [VocabularyWord(english=word).to_dict() for word in sorted(vocabulary)]
    
    # Create the final structure
    result = {
        "group": {"name": group_name},
        "words": vocab_words
    }
    
    return result