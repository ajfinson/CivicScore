"""Tenant domain model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Tenant:
    """Represents a tenant (city, building, campus, etc.)"""
    id: Optional[int]
    name: str
    type: str  # city, building, campus, hotel, facility
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def display_name(self) -> str:
        """Get formatted display name"""
        return f"{self.name} ({self.type.title()})"
