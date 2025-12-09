"""CRUD SQL methods"""
from sqlalchemy.orm import Session
from app.db.models import TenantModel, AreaModel, IssueModel, ReportModel
from typing import List, Optional


class TenantRepository:
    """Repository for tenant operations"""
    
    @staticmethod
    def create(db: Session, name: str, type: str) -> TenantModel:
        """Create a new tenant"""
        tenant = TenantModel(name=name, type=type)
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant
    
    @staticmethod
    def get_by_id(db: Session, tenant_id: int) -> Optional[TenantModel]:
        """Get tenant by ID"""
        return db.query(TenantModel).filter(TenantModel.id == tenant_id).first()
    
    @staticmethod
    def list_all(db: Session) -> List[TenantModel]:
        """List all tenants"""
        return db.query(TenantModel).all()


class IssueRepository:
    """Repository for issue operations"""
    
    @staticmethod
    def create(db: Session, tenant_id: int, category: str, severity: str, 
               area_id: Optional[int] = None) -> IssueModel:
        """Create a new issue"""
        issue = IssueModel(
            tenant_id=tenant_id,
            area_id=area_id,
            category=category,
            severity=severity
        )
        db.add(issue)
        db.commit()
        db.refresh(issue)
        return issue
    
    @staticmethod
    def get_by_id(db: Session, issue_id: int) -> Optional[IssueModel]:
        """Get issue by ID"""
        return db.query(IssueModel).filter(IssueModel.id == issue_id).first()
    
    @staticmethod
    def list_by_tenant(db: Session, tenant_id: int, status: Optional[str] = None) -> List[IssueModel]:
        """List issues for a tenant"""
        query = db.query(IssueModel).filter(IssueModel.tenant_id == tenant_id)
        if status:
            query = query.filter(IssueModel.status == status)
        return query.all()


class ReportRepository:
    """Repository for report operations"""
    
    @staticmethod
    def create(db: Session, tenant_id: int, description: str, 
               location: Optional[str] = None) -> ReportModel:
        """Create a new report"""
        report = ReportModel(
            tenant_id=tenant_id,
            description=description,
            location=location
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    
    @staticmethod
    def get_unprocessed(db: Session, limit: int = 100) -> List[ReportModel]:
        """Get unprocessed reports"""
        return db.query(ReportModel).filter(
            ReportModel.processed == False
        ).limit(limit).all()
    
    @staticmethod
    def link_to_issue(db: Session, report_id: int, issue_id: int):
        """Link a report to an issue"""
        report = db.query(ReportModel).filter(ReportModel.id == report_id).first()
        if report:
            report.issue_id = issue_id
            report.processed = True
            db.commit()
