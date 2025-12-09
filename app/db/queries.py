"""Optimized analytic SQL queries"""
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from app.db.models import IssueModel, ReportModel, SLAMetricModel, PerformanceScoreModel
from datetime import datetime, timedelta


def get_issue_counts_by_category(db: Session, tenant_id: int) -> dict:
    """Get issue counts grouped by category"""
    results = db.query(
        IssueModel.category,
        func.count(IssueModel.id).label('count')
    ).filter(
        IssueModel.tenant_id == tenant_id
    ).group_by(
        IssueModel.category
    ).all()
    
    return {row.category: row.count for row in results}


def get_sla_compliance_rate(db: Session, tenant_id: int, days: int = 30) -> float:
    """Calculate SLA compliance rate for a tenant"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = db.query(
        func.avg(case((SLAMetricModel.met_sla == True, 1.0), else_=0.0)).label('compliance_rate')
    ).join(
        IssueModel
    ).filter(
        IssueModel.tenant_id == tenant_id,
        SLAMetricModel.calculated_at >= cutoff_date
    ).scalar()
    
    return result or 0.0


def get_average_resolution_time(db: Session, tenant_id: int, days: int = 30) -> float:
    """Get average resolution time in hours"""
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    result = db.query(
        func.avg(SLAMetricModel.resolution_time_hours).label('avg_time')
    ).join(
        IssueModel
    ).filter(
        IssueModel.tenant_id == tenant_id,
        SLAMetricModel.calculated_at >= cutoff_date
    ).scalar()
    
    return result or 0.0


def get_open_issues_count(db: Session, tenant_id: int) -> int:
    """Get count of open issues"""
    return db.query(func.count(IssueModel.id)).filter(
        IssueModel.tenant_id == tenant_id,
        IssueModel.status == 'open'
    ).scalar()
