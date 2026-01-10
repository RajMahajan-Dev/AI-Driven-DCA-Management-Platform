from datetime import datetime, timedelta
from app.models import Priority, SLAStatus, CaseStatus


class WorkflowEngine:
    """Rule-based workflow engine for case management."""
    
    # SLA days by priority
    SLA_DAYS = {
        Priority.P1: 3,   # 3 days for P1
        Priority.P2: 7,   # 7 days for P2
        Priority.P3: 14,  # 14 days for P3
    }
    
    # Priority thresholds
    P1_AMOUNT_THRESHOLD = 50000  # Amount >= 50k
    P1_AGEING_THRESHOLD = 90     # Ageing >= 90 days
    P2_AMOUNT_THRESHOLD = 20000  # Amount >= 20k
    P2_AGEING_THRESHOLD = 60     # Ageing >= 60 days
    
    @staticmethod
    def calculate_priority(overdue_amount: float, ageing_days: int) -> Priority:
        """
        Calculate case priority based on overdue amount and ageing days.
        
        Rules:
        - P1: Amount >= 50k OR Ageing >= 90 days
        - P2: Amount >= 20k OR Ageing >= 60 days
        - P3: All other cases
        """
        if (overdue_amount >= WorkflowEngine.P1_AMOUNT_THRESHOLD or 
            ageing_days >= WorkflowEngine.P1_AGEING_THRESHOLD):
            return Priority.P1
        elif (overdue_amount >= WorkflowEngine.P2_AMOUNT_THRESHOLD or 
              ageing_days >= WorkflowEngine.P2_AGEING_THRESHOLD):
            return Priority.P2
        else:
            return Priority.P3
    
    @staticmethod
    def calculate_sla_due_date(priority: Priority, created_at: datetime = None) -> datetime:
        """Calculate SLA due date based on priority."""
        if created_at is None:
            created_at = datetime.utcnow()
        
        sla_days = WorkflowEngine.SLA_DAYS[priority]
        return created_at + timedelta(days=sla_days)
    
    @staticmethod
    def calculate_sla_status(sla_due_date: datetime) -> SLAStatus:
        """
        Calculate SLA status based on due date.
        
        Rules:
        - Breached: Past due date
        - At Risk: Within 24 hours of due date
        - On Track: More than 24 hours remaining
        """
        now = datetime.utcnow()
        time_remaining = sla_due_date - now
        
        if time_remaining.total_seconds() < 0:
            return SLAStatus.BREACHED
        elif time_remaining.total_seconds() < 86400:  # 24 hours in seconds
            return SLAStatus.AT_RISK
        else:
            return SLAStatus.ON_TRACK
    
    @staticmethod
    def validate_status_transition(current_status: CaseStatus, new_status: CaseStatus) -> tuple[bool, str]:
        """
        Validate status transition rules.
        
        Allowed transitions:
        - Open -> In Progress
        - Open -> Closed
        - In Progress -> Closed
        - In Progress -> Open (re-open)
        """
        allowed_transitions = {
            CaseStatus.OPEN: [CaseStatus.IN_PROGRESS, CaseStatus.CLOSED],
            CaseStatus.IN_PROGRESS: [CaseStatus.CLOSED, CaseStatus.OPEN],
            CaseStatus.CLOSED: [],  # Closed cases cannot be transitioned
        }
        
        if current_status == new_status:
            return True, "No status change"
        
        if new_status in allowed_transitions.get(current_status, []):
            return True, f"Valid transition from {current_status} to {new_status}"
        else:
            return False, f"Invalid transition from {current_status} to {new_status}"
    
    @staticmethod
    def get_priority_score(priority: Priority) -> int:
        """Get numeric score for priority (higher = more urgent)."""
        priority_scores = {
            Priority.P1: 3,
            Priority.P2: 2,
            Priority.P3: 1,
        }
        return priority_scores[priority]
