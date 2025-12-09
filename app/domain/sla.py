"""SLA domain model"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass
class SLA:
    """Represents an SLA metric"""
    id: Optional[int]
    issue_id: int
    resolution_time_hours: Optional[float]
    met_sla: bool
    calculated_at: datetime = None
    
    def __post_init__(self):
        if self.calculated_at is None:
            self.calculated_at = datetime.now()
    
    @staticmethod
    def calculate_resolution_time(created_at: datetime, resolved_at: datetime) -> float:
        """Calculate resolution time in hours"""
        delta = resolved_at - created_at
        return delta.total_seconds() / 3600
    
    @staticmethod
    def check_sla_compliance(resolution_hours: float, threshold_hours: float) -> bool:
        """Check if resolution met SLA threshold"""
        return resolution_hours <= threshold_hours
