from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from app.models import Case, DCA, AuditLog, User, CaseStatus, Priority, SLAStatus
from app.schemas import CaseCreate, CaseUpdate, DashboardStats
from app.workflows import WorkflowEngine
from app.ai import get_predictor


class CaseService:
    """Service layer for case management operations."""
    
    @staticmethod
    def create_case(db: Session, case_data: CaseCreate, user: User) -> Case:
        """Create a new case with automated workflow rules."""
        # Generate unique case ID
        case_count = db.query(Case).count()
        case_id = f"CASE-{datetime.utcnow().year}-{case_count + 1:06d}"
        
        # Calculate priority using workflow engine
        priority = WorkflowEngine.calculate_priority(
            case_data.overdue_amount,
            case_data.ageing_days
        )
        
        # Calculate SLA due date
        sla_due_date = WorkflowEngine.calculate_sla_due_date(priority)
        
        # Calculate SLA status
        sla_status = WorkflowEngine.calculate_sla_status(sla_due_date)
        
        # Predict AI recovery score
        predictor = get_predictor()
        ai_score = predictor.predict_recovery_score(
            case_data.overdue_amount,
            case_data.ageing_days
        )
        
        # Create case
        case = Case(
            case_id=case_id,
            customer_name=case_data.customer_name,
            customer_email=case_data.customer_email,
            customer_phone=case_data.customer_phone,
            overdue_amount=case_data.overdue_amount,
            ageing_days=case_data.ageing_days,
            status=CaseStatus.OPEN,
            priority=priority,
            sla_due_date=sla_due_date,
            sla_status=sla_status,
            ai_recovery_score=ai_score,
            notes=case_data.notes
        )
        
        db.add(case)
        db.flush()
        
        # Allocate to DCA
        CaseService._allocate_to_dca(db, case)
        
        # Create audit log
        AuditLog.create_log(
            db=db,
            user_id=user.id,
            case_id=case.id,
            action_type="CREATE_CASE",
            description=f"Created case {case_id}",
            new_value=f"Priority: {priority}, Amount: {case_data.overdue_amount}"
        )
        
        db.commit()
        db.refresh(case)
        return case
    
    @staticmethod
    def _allocate_to_dca(db: Session, case: Case):
        """Allocate case to best available DCA."""
        # Get active DCAs with capacity
        dcas = db.query(DCA).filter(
            DCA.is_active == True,
            DCA.active_cases_count < DCA.max_capacity
        ).order_by(
            DCA.performance_score.desc(),
            DCA.active_cases_count.asc()
        ).all()
        
        if not dcas:
            case.allocation_reason = "No available DCA with capacity"
            return
        
        # Allocation logic:
        # - P1 cases go to best performing DCA
        # - P2/P3 use load balancing
        if case.priority == Priority.P1:
            selected_dca = dcas[0]  # Best performing
            reason = f"High priority case assigned to best performing DCA (score: {selected_dca.performance_score})"
        else:
            # Load balance - find DCA with lowest active cases
            selected_dca = min(dcas, key=lambda d: d.active_cases_count)
            reason = f"Load balanced to DCA with {selected_dca.active_cases_count} active cases"
        
        # Assign DCA
        case.dca_id = selected_dca.id
        case.allocation_reason = reason
        
        # Update DCA case count
        selected_dca.active_cases_count += 1
    
    @staticmethod
    def get_case(db: Session, case_id: int) -> Optional[Case]:
        """Get case by ID."""
        return db.query(Case).filter(Case.id == case_id).first()
    
    @staticmethod
    def get_case_by_case_id(db: Session, case_id: str) -> Optional[Case]:
        """Get case by case_id string."""
        return db.query(Case).filter(Case.case_id == case_id).first()
    
    @staticmethod
    def list_cases(
        db: Session,
        status: Optional[CaseStatus] = None,
        priority: Optional[Priority] = None,
        sla_status: Optional[SLAStatus] = None,
        dca_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Case]:
        """List cases with optional filters."""
        query = db.query(Case)
        
        if status:
            query = query.filter(Case.status == status)
        if priority:
            query = query.filter(Case.priority == priority)
        if sla_status:
            query = query.filter(Case.sla_status == sla_status)
        if dca_id:
            query = query.filter(Case.dca_id == dca_id)
        
        return query.order_by(Case.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_case_status(
        db: Session,
        case_id: int,
        new_status: CaseStatus,
        user: User,
        notes: Optional[str] = None
    ) -> Case:
        """Update case status with validation."""
        case = CaseService.get_case(db, case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        
        # Validate transition
        valid, message = WorkflowEngine.validate_status_transition(case.status, new_status)
        if not valid:
            raise ValueError(message)
        
        old_status = case.status
        case.status = new_status
        
        if notes:
            case.notes = f"{case.notes}\n{notes}" if case.notes else notes
        
        # Update DCA case count if closing
        if new_status == CaseStatus.CLOSED and case.dca_id:
            dca = db.query(DCA).filter(DCA.id == case.dca_id).first()
            if dca:
                dca.active_cases_count = max(0, dca.active_cases_count - 1)
        
        # Create audit log
        AuditLog.create_log(
            db=db,
            user_id=user.id,
            case_id=case.id,
            action_type="UPDATE_STATUS",
            description=f"Status changed from {old_status} to {new_status}",
            old_value=old_status.value,
            new_value=new_status.value
        )
        
        db.commit()
        db.refresh(case)
        return case
    
    @staticmethod
    def update_sla_statuses(db: Session):
        """Batch update SLA statuses for all open cases."""
        cases = db.query(Case).filter(
            Case.status.in_([CaseStatus.OPEN, CaseStatus.IN_PROGRESS])
        ).all()
        
        for case in cases:
            new_sla_status = WorkflowEngine.calculate_sla_status(case.sla_due_date)
            if case.sla_status != new_sla_status:
                case.sla_status = new_sla_status
        
        db.commit()
    
    @staticmethod
    def escalate_case(db: Session, case_id: int, user: User, reason: str) -> Case:
        """Manually escalate a case."""
        case = CaseService.get_case(db, case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        
        # Create audit log for escalation
        AuditLog.create_log(
            db=db,
            user_id=user.id,
            case_id=case.id,
            action_type="ESCALATE_CASE",
            description=f"Case manually escalated: {reason}",
            new_value=reason
        )
        
        db.commit()
        db.refresh(case)
        return case
    
    @staticmethod
    def get_dashboard_stats(db: Session) -> DashboardStats:
        """Get dashboard statistics."""
        # Total overdue amount
        total_overdue = db.query(func.sum(Case.overdue_amount)).filter(
            Case.status != CaseStatus.CLOSED
        ).scalar() or 0
        
        # Total cases
        total_cases = db.query(Case).count()
        
        # Cases by status
        open_cases = db.query(Case).filter(Case.status == CaseStatus.OPEN).count()
        in_progress_cases = db.query(Case).filter(Case.status == CaseStatus.IN_PROGRESS).count()
        closed_cases = db.query(Case).filter(Case.status == CaseStatus.CLOSED).count()
        
        # Pending cases (OPEN + IN_PROGRESS)
        pending_cases = open_cases + in_progress_cases
        
        # Rejected cases - cases that were unassigned from DCA
        # For now, we'll approximate this as cases that had dca_id but now don't (or track separately)
        rejected_cases = 0  # Can be enhanced with proper tracking
        
        # Amount calculations
        pending_amount = db.query(func.sum(Case.overdue_amount)).filter(
            Case.status.in_([CaseStatus.OPEN, CaseStatus.IN_PROGRESS])
        ).scalar() or 0
        
        recovered_amount = db.query(func.sum(Case.overdue_amount)).filter(
            Case.status == CaseStatus.CLOSED
        ).scalar() or 0
        
        # SLA breach count
        sla_breach_count = db.query(Case).filter(
            Case.sla_status == SLAStatus.BREACHED,
            Case.status != CaseStatus.CLOSED
        ).count()
        
        # At risk count
        at_risk_count = db.query(Case).filter(
            Case.sla_status == SLAStatus.AT_RISK,
            Case.status != CaseStatus.CLOSED
        ).count()
        
        # DCA stats
        total_dcas = db.query(DCA).count()
        active_dcas = db.query(DCA).filter(DCA.is_active == True).count()
        
        return DashboardStats(
            total_overdue_amount=float(total_overdue),
            total_cases=total_cases,
            open_cases=open_cases,
            in_progress_cases=in_progress_cases,
            closed_cases=closed_cases,
            sla_breach_count=sla_breach_count,
            at_risk_count=at_risk_count,
            total_dcas=total_dcas,
            active_dcas=active_dcas,
            rejected_cases=rejected_cases,
            pending_cases=pending_cases,
            pending_amount=float(pending_amount),
            recovered_amount=float(recovered_amount)
        )


# Add helper method to AuditLog model
def create_audit_log(
    db: Session,
    user_id: int,
    case_id: Optional[int],
    action_type: str,
    description: Optional[str] = None,
    old_value: Optional[str] = None,
    new_value: Optional[str] = None
):
    """Helper to create audit log."""
    log = AuditLog(
        user_id=user_id,
        case_id=case_id,
        action_type=action_type,
        description=description,
        old_value=old_value,
        new_value=new_value
    )
    db.add(log)
    return log


# Monkey patch the method onto AuditLog
AuditLog.create_log = staticmethod(create_audit_log)
