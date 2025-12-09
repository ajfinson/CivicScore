"""Report domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Report:
    """Represents an individual incident report"""
    id: Optional[int]
    issue_id: Optional[int]
    tenant_id: int
    description: str
    location: Optional[str]
    submitted_at: datetime = None
    processed: bool = False
    
    def __post_init__(self):
        if self.submitted_at is None:
            self.submitted_at = datetime.now()
    
    def mark_processed(self, issue_id: int):
        """Mark report as processed and link to issue"""
        self.processed = True
        self.issue_id = issue_id
