"""Location clustering helpers"""
import re
from typing import List, Optional


def parse_location(location_str: str) -> dict:
    """Parse location string into structured components"""
    # TODO: Extract street, intersection, building, etc.
    return {
        "raw": location_str,
        "street": None,
        "intersection": None,
        "building": None
    }


def calculate_distance(loc1: dict, loc2: dict) -> float:
    """Calculate distance between two locations"""
    # TODO: Implement distance calculation
    # For MVP, could use simple string similarity
    return 0.0


def cluster_locations(locations: List[str], threshold: float = 0.8) -> List[List[str]]:
    """Group similar locations into clusters"""
    # TODO: Implement location clustering algorithm
    return []


def normalize_location(location: str) -> str:
    """Normalize location string for comparison"""
    # Convert to lowercase, remove extra spaces
    normalized = location.lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Standardize common abbreviations
    replacements = {
        'street': 'st',
        'avenue': 'ave',
        'road': 'rd',
        'boulevard': 'blvd'
    }
    
    for full, abbrev in replacements.items():
        normalized = normalized.replace(full, abbrev)
    
    return normalized
