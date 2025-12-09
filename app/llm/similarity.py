"""Matching reports to existing issues"""
from app.llm.client import llm_client


def find_similar_report(new_report: str, existing_issues: list) -> dict:
    """Find which existing issue (if any) matches a new report"""
    
    if not existing_issues:
        return {"match": False, "issue_id": None, "confidence": 0.0}
    
    issues_text = "\n".join([
        f"Issue {issue['id']}: {issue['description']}"
        for issue in existing_issues[:10]  # Limit to avoid token limits
    ])
    
    prompt = f"""
You are matching a new incident report to existing open issues.

New Report: {new_report}

Existing Open Issues:
{issues_text}

Respond with JSON:
- match: true if the new report is essentially the same issue as an existing one
- issue_id: the ID of the matching issue (or null if no match)
- confidence: 0.0 to 1.0 indicating match confidence
- reasoning: brief explanation of your decision

Example:
{{
    "match": true,
    "issue_id": 5,
    "confidence": 0.85,
    "reasoning": "Both reports describe the same pothole at Main and 1st"
}}
"""
    
    try:
        result = llm_client.complete_json(prompt)
        return result
    except Exception as e:
        print(f"Error finding similar reports: {e}")
        return {"match": False, "issue_id": None, "confidence": 0.0}
