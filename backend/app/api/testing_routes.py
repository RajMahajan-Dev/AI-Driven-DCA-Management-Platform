from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timezone

from app.database import get_db
from app.models import Case, DCA, CaseStatus, User
from app.auth import get_current_user
from app.utils.performance import calculate_dca_performance_score, update_active_case_count
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/testing", tags=["Testing"])


class CaseStatusUpdate(BaseModel):
    case_id: int
    status: CaseStatus
    confirmation_received: bool = False


@router.get("/cases")
def get_all_cases_for_testing(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all cases with DCA information for testing."""
    cases = db.query(Case).all()
    
    result = []
    for case in cases:
        result.append({
            "id": case.id,
            "case_id": case.case_id,
            "customer_name": case.customer_name,
            "overdue_amount": case.overdue_amount,
            "status": case.status.value,
            "priority": case.priority.value,
            "dca_name": case.dca.name if case.dca else "Unassigned",
            "dca_id": case.dca_id,
            "confirmation_received": case.confirmation_received,
            "created_at": case.created_at,
            "assigned_at": case.assigned_at
        })
    
    return result


@router.post("/update-status")
def update_case_status_testing(
    update: CaseStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update case status from DCA testing interface."""
    case = db.query(Case).options(joinedload(Case.dca)).filter(Case.id == update.case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    old_status = case.status
    case.status = update.status
    case.confirmation_received = update.confirmation_received
    
    # Update completion metrics
    if update.status == CaseStatus.CLOSED and not case.completed_at:
        case.completed_at = datetime.now(timezone.utc)
        
        # Update DCA performance metrics only if case is assigned to a DCA
        if case.dca_id and case.dca and case.assigned_at:
            dca = case.dca
            dca.total_cases_completed += 1
            
            # Recalculate performance score using new logic
            score = calculate_dca_performance_score(dca, db)
            dca.performance_score = str(score) if isinstance(score, (int, float)) else score
            
            # Update active case count (remove completed from active)
            update_active_case_count(dca, db)
    
    db.commit()
    db.refresh(case)
    
    return {
        "message": "Status updated successfully",
        "case_id": case.case_id,
        "old_status": old_status.value,
        "new_status": case.status.value,
        "confirmation_received": case.confirmation_received
    }


@router.get("/dcas")
def get_all_dcas_for_testing(db: Session = Depends(get_db)):
    """Get all DCAs with their performance metrics."""
    dcas = db.query(DCA).all()
    
    result = []
    for dca in dcas:
        result.append({
            "id": dca.id,
            "name": dca.name,
            "performance_score": dca.performance_score,
            "active_cases": dca.active_cases_count,
            "total_completed": dca.total_cases_completed,
            "total_rejected": dca.total_cases_rejected,
            "total_delays": dca.total_delays,
            "avg_completion_time": dca.avg_completion_time_days,
            "min_debt": dca.min_debt_amount,
            "max_debt": dca.max_debt_amount
        })
    
    return result


@router.post("/simulate-rejection/{case_id}")
def simulate_case_rejection(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Simulate a DCA rejecting a case and auto-reassign to another DCA."""
    case = db.query(Case).options(joinedload(Case.dca)).filter(Case.id == case_id).first()
    
    if not case or not case.dca:
        raise HTTPException(status_code=404, detail="Case or DCA not found")
    
    old_dca = case.dca
    old_dca.total_cases_rejected += 1
    
    # Recalculate performance score after rejection
    score = calculate_dca_performance_score(old_dca, db)
    old_dca.performance_score = str(score) if isinstance(score, (int, float)) else score
    
    # Update active case count
    update_active_case_count(old_dca, db)
    
    # Add rejection note
    case.notes = (case.notes or "") + f"\n[{datetime.now(timezone.utc)}] Case rejected by {old_dca.name}"
    
    # Auto-reassign to another DCA
    all_dcas = db.query(DCA).filter(
        DCA.id != old_dca.id,
        DCA.is_active == True,
        DCA.active_cases_count < DCA.max_capacity
    ).all()
    
    if all_dcas:
        # Find suitable DCA based on debt range
        suitable_dcas = [
            dca for dca in all_dcas
            if dca.min_debt_amount <= case.overdue_amount <= dca.max_debt_amount
        ]
        
        if suitable_dcas:
            new_dca = suitable_dcas[0]  # Pick first suitable DCA
        else:
            new_dca = all_dcas[0]  # Pick any available DCA
        
        case.dca_id = new_dca.id
        case.assigned_at = datetime.now(timezone.utc)
        case.allocation_reason = f"Auto-reassigned after rejection by {old_dca.name}"
        new_dca.active_cases_count += 1
        
        case.notes += f"\n[{datetime.now(timezone.utc)}] Auto-reassigned to {new_dca.name}"
        
        db.commit()
        return {
            "message": f"Case rejected by {old_dca.name} and reassigned to {new_dca.name}",
            "case_id": case.case_id,
            "new_dca": new_dca.name
        }
    else:
        # No available DCA - unassign
        case.dca_id = None
        case.notes += f"\n[{datetime.now(timezone.utc)}] No available DCA for reassignment"
        db.commit()
        return {
            "message": f"Case rejected by {old_dca.name}. No available DCA for reassignment.",
            "case_id": case.case_id
        }


@router.post("/simulate-delay/{case_id}")
def simulate_case_delay(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Simulate a delay in case processing."""
    case = db.query(Case).options(joinedload(Case.dca)).filter(Case.id == case_id).first()
    
    if not case or not case.dca:
        raise HTTPException(status_code=404, detail="Case or DCA not found")
    
    dca = case.dca
    dca.total_delays += 1
    
    # Recalculate performance score after delay
    score = calculate_dca_performance_score(dca, db)
    dca.performance_score = str(score) if isinstance(score, (int, float)) else score
    
    case.notes = (case.notes or "") + f"\n[{datetime.now(timezone.utc)}] Delay reported by {dca.name}"
    
    db.commit()
    
    return {"message": f"Delay recorded for {dca.name}", "case_id": case.case_id}


@router.post("/reset-data")
def reset_dummy_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reset all dummy data for testing purposes."""
    try:
        # Import the init function
        from app.init_dummy_data import init_comprehensive_dummy_data
        
        # Clear existing data
        db.query(Case).delete()
        db.query(DCA).delete()
        db.commit()
        
        # Reinitialize dummy data
        init_comprehensive_dummy_data()
        
        return {"message": "All dummy data has been reset successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to reset data: {str(e)}")
