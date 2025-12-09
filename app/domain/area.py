"""Area domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Area:
    """Represents an area/zone within a tenant"""
    id: Optional[int]
    tenant_id: int
    name: str
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
