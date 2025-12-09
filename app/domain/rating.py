"""Rating/score domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Rating:
    """Represents a performance rating/score"""
    id: Optional[int]
    tenant_id: int
    area_id: Optional[int]
    score: float
    metric_type: str
    calculated_at: datetime = None
    
    def __post_init__(self):
        if self.calculated_at is None:
            self.calculated_at = datetime.now()
    
    @property
    def letter_grade(self) -> str:
        """Convert numeric score to letter grade"""
        if self.score >= 90:
            return "A"
        elif self.score >= 80:
            return "B"
        elif self.score >= 70:
            return "C"
        elif self.score >= 60:
            return "D"
        else:
            return "F"
