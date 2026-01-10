from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import DashboardStats, AuditLogResponse
from app.models import User, AuditLog
from app.services import CaseService
from app.auth import get_current_active_user

router = APIRouter(prefix="/api/v1", tags=["Dashboard"])


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get dashboard statistics."""
    stats = CaseService.get_dashboard_stats(db)
    return stats


@router.get("/audit-logs", response_model=List[AuditLogResponse])
def get_audit_logs(
    case_id: int = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get audit logs with optional case filter."""
    query = db.query(AuditLog)
    
    if case_id:
        query = query.filter(AuditLog.case_id == case_id)
    
    logs = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
    return logs
