"""ORM models per table"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, DECIMAL, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class TenantModel(Base):
    __tablename__ = "tenants"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    areas = relationship("AreaModel", back_populates="tenant")
    issues = relationship("IssueModel", back_populates="tenant")


class AreaModel(Base):
    __tablename__ = "areas"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    tenant = relationship("TenantModel", back_populates="areas")
    issues = relationship("IssueModel", back_populates="area")


class IssueModel(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    area_id = Column(Integer, ForeignKey("areas.id"))
    category = Column(String(100))
    severity = Column(String(50))
    status = Column(String(50), default="open", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    tenant = relationship("TenantModel", back_populates="issues")
    area = relationship("AreaModel", back_populates="issues")
    reports = relationship("ReportModel", back_populates="issue")
    sla_metrics = relationship("SLAMetricModel", back_populates="issue")


class ReportModel(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), index=True)
    description = Column(Text, nullable=False)
    location = Column(String(255))
    submitted_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    
    issue = relationship("IssueModel", back_populates="reports")


class SLAMetricModel(Base):
    __tablename__ = "sla_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, ForeignKey("issues.id"), index=True)
    resolution_time_hours = Column(DECIMAL)
    met_sla = Column(Boolean)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    issue = relationship("IssueModel", back_populates="sla_metrics")


class PerformanceScoreModel(Base):
    __tablename__ = "performance_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))
    score = Column(DECIMAL, nullable=False)
    metric_type = Column(String(100))
    calculated_at = Column(DateTime, default=datetime.utcnow)
