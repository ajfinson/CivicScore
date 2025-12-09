"""Tenant/area leaderboards"""
from typing import List, Dict


def compute_tenant_rankings(metric_type: str = "overall") -> List[Dict]:
    """Compute rankings across all tenants"""
    # TODO: Query performance scores
    # TODO: Rank tenants by score
    # TODO: Return sorted leaderboard
    
    return []


def compute_area_rankings(tenant_id: int) -> List[Dict]:
    """Compute rankings for areas within a tenant"""
    # TODO: Query area-level scores
    # TODO: Rank areas by performance
    
    return []


def get_percentile_rank(score: float, all_scores: List[float]) -> float:
    """Calculate percentile rank for a score"""
    if not all_scores:
        return 50.0
    
    sorted_scores = sorted(all_scores)
    rank = sum(1 for s in sorted_scores if s <= score)
    percentile = (rank / len(sorted_scores)) * 100
    return round(percentile, 1)
