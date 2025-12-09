"""Text normalization helpers"""
import re
from typing import List


def normalize_text(text: str) -> str:
    """Normalize text for comparison"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text.strip()


def remove_stopwords(text: str) -> str:
    """Remove common stopwords from text"""
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for'}
    words = text.split()
    filtered = [w for w in words if w.lower() not in stopwords]
    return ' '.join(filtered)


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract key terms from text"""
    # TODO: Implement more sophisticated keyword extraction
    # For now, just split and take most common non-stopword terms
    normalized = normalize_text(text)
    words = normalized.split()
    
    # Filter out very short words
    keywords = [w for w in words if len(w) > 3]
    
    # Return unique keywords
    return list(set(keywords))[:max_keywords]


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two text strings"""
    # Simple Jaccard similarity on word sets
    words1 = set(normalize_text(text1).split())
    words2 = set(normalize_text(text2).split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0
