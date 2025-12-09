"""Issue domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Issue:
    """Represents a grouped incident issue"""
    id: Optional[int]
    tenant_id: int
    area_id: Optional[int]
    category: str
    severity: str
    status: str = "open"
    created_at: datetime = None
    resolved_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def resolve(self):
        """Mark issue as resolved"""
        self.status = "resolved"
        self.resolved_at = datetime.now()
    
    def is_open(self) -> bool:
        """Check if issue is still open"""
        return self.status == "open"
