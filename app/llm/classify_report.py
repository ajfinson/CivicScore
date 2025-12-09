"""Category + severity detection prompts"""
from app.llm.client import llm_client


def classify_report(description: str, location: str = None) -> dict:
    """Classify a report using LLM"""
    
    prompt = f"""
You are analyzing a civic incident report. Classify it and extract key information.

Report Description: {description}
Location: {location or "Not specified"}

Respond with JSON containing:
- category: One of [infrastructure, sanitation, safety, noise, maintenance, other]
- severity: One of [low, medium, high, critical]
- summary: A brief 1-sentence summary
- suggested_area: If you can infer a specific area/zone from the description

Example response format:
{{
    "category": "infrastructure",
    "severity": "high",
    "summary": "Broken traffic light at Main St intersection",
    "suggested_area": "downtown"
}}
"""
    
    try:
        result = llm_client.complete_json(prompt)
        return result
    except Exception as e:
        print(f"Error classifying report: {e}")
        return {
            "category": "other",
            "severity": "medium",
            "summary": description[:100],
            "suggested_area": None
        }
