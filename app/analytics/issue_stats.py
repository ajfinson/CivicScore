"""Issue counts & trends"""
from datetime import datetime, timedelta
from typing import Dict


def compute_issue_stats(tenant_id: int, days: int = 30) -> Dict:
    """Compute issue statistics for a tenant"""
    # TODO: Query database for issue data
    # TODO: Calculate counts, trends, and distributions
    
    return {
        "total_issues": 0,
        "open_issues": 0,
        "resolved_issues": 0,
        "by_category": {},
        "by_severity": {},
        "trend": "stable"  # increasing, decreasing, stable
    }


def compute_trend(current_count: int, previous_count: int) -> str:
    """Determine trend direction"""
    if current_count > previous_count * 1.1:
        return "increasing"
    elif current_count < previous_count * 0.9:
        return "decreasing"
    else:
        return "stable"
