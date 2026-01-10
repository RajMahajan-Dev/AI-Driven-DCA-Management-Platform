from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.schemas import CaseCreate, CaseUpdate, CaseResponse, EscalationRequest
from app.models import User, CaseStatus, Priority, SLAStatus, RoleEnum
from app.services import CaseService
from app.auth import get_current_active_user, require_role

router = APIRouter(prefix="/api/v1/cases", tags=["Cases"])


@router.post("/", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new case."""
    try:
        case = CaseService.create_case(db, case_data, current_user)
        return case
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CaseResponse])
def list_cases(
    status: Optional[CaseStatus] = None,
    priority: Optional[Priority] = None,
    sla_status: Optional[SLAStatus] = None,
    dca_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List cases with optional filters."""
    cases = CaseService.list_cases(
        db=db,
        status=status,
        priority=priority,
        sla_status=sla_status,
        dca_id=dca_id,
        skip=skip,
        limit=limit
    )
    return cases


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get case by ID."""
    case = CaseService.get_case(db, case_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case {case_id} not found"
        )
    return case


@router.patch("/{case_id}/status", response_model=CaseResponse)
def update_case_status(
    case_id: int,
    update_data: CaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update case status."""
    if not update_data.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required"
        )
    
    try:
        case = CaseService.update_case_status(
            db=db,
            case_id=case_id,
            new_status=update_data.status,
            user=current_user,
            notes=update_data.notes
        )
        return case
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{case_id}/escalate", response_model=CaseResponse)
def escalate_case(
    case_id: int,
    escalation: EscalationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Manually escalate a case."""
    try:
        case = CaseService.escalate_case(db, case_id, current_user, escalation.reason)
        return case
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/update-sla-statuses", status_code=status.HTTP_200_OK)
def update_sla_statuses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([RoleEnum.ADMIN]))
):
    """Batch update SLA statuses for all cases (Admin only)."""
    CaseService.update_sla_statuses(db)
    return {"message": "SLA statuses updated successfully"}
