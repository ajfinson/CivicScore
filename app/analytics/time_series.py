"""Historical trend builders"""
from datetime import datetime, timedelta
from typing import List, Dict


def build_time_series(tenant_id: int, metric: str, days: int = 30) -> List[Dict]:
    """Build time series data for a metric"""
    # TODO: Query historical data points
    # TODO: Group by time intervals (daily, weekly)
    # TODO: Return time series array
    
    return []


def aggregate_by_interval(data: List[Dict], interval: str = "daily") -> List[Dict]:
    """Aggregate data points by time interval"""
    # TODO: Group data by day/week/month
    # TODO: Calculate aggregates (sum, avg, etc.)
    
    return []


def smooth_trend(values: List[float], window_size: int = 7) -> List[float]:
    """Apply moving average smoothing to trend data"""
    if len(values) < window_size:
        return values
    
    smoothed = []
    for i in range(len(values)):
        start = max(0, i - window_size + 1)
        end = i + 1
        window = values[start:end]
        smoothed.append(sum(window) / len(window))
    
    return smoothed
