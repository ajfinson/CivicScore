"""JSON schema validation of LLM results"""
from typing import Any


def validate_classification(data: dict) -> bool:
    """Validate classification response structure"""
    required_fields = ["category", "severity", "summary"]
    valid_categories = ["infrastructure", "sanitation", "safety", "noise", "maintenance", "other"]
    valid_severities = ["low", "medium", "high", "critical"]
    
    if not all(field in data for field in required_fields):
        return False
    
    if data["category"] not in valid_categories:
        return False
    
    if data["severity"] not in valid_severities:
        return False
    
    return True


def validate_similarity_result(data: dict) -> bool:
    """Validate similarity matching response"""
    required_fields = ["match", "confidence"]
    
    if not all(field in data for field in required_fields):
        return False
    
    if not isinstance(data["match"], bool):
        return False
    
    if not (0.0 <= data["confidence"] <= 1.0):
        return False
    
    return True
