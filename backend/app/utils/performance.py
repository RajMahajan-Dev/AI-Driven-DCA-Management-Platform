"""
Performance Score Calculation Utilities
Calculates DCA performance scores based on:
- 100% base score for perfect completion
- Penalties: Rejection (-5%), Delay (-3%), At Risk (-5%), Breached (-5%), Processing time over 10 days (-2%/day)
- Rewards: Quick completion within 5 days (+5%)
- Average time from case assignment to completion
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Case, DCA, CaseStatus, SLAStatus


def calculate_dca_performance_score(dca: DCA, db: Session) -> float:
    """
    Calculate DCA performance score based on their case handling.
    
    Scoring Logic:
    - Start with 100% base score
    - For each COMPLETED case:
      * Reward: +5% if completed within 5 days (quick resolution)
      * Penalty: -2% per day if completed in more than 10 days
      * Penalty: -5% if case was AT_RISK at completion
      * Penalty: -5% if case was BREACHED at completion
    - For REJECTIONS: -5% per rejected case
    - For DELAYS: -3% per delayed case
    
    Args:
        dca: DCA instance
        db: Database session
        
    Returns:
        float: Performance score (0-100) or "TBD"
    """
    
    # Get all completed cases handled by this DCA
    completed_cases = db.query(Case).filter(
        Case.dca_id == dca.id,
        Case.status == CaseStatus.CLOSED
    ).all()
    
    # If no completed cases, return TBD
    if not completed_cases:
        return "TBD"
    
    # Start with 100% base score
    base_score = 100.0
    total_rewards = 0.0
    total_penalties = 0.0
    
    # Analyze completed cases
    total_completed = len(completed_cases)
    total_completion_days = 0
    quick_completions = 0
    at_risk_cases = 0
    breached_cases = 0
    slow_completions = 0
    
    for case in completed_cases:
        # Calculate processing time (from assigned_at to completed_at)
        if case.assigned_at and case.completed_at:
            processing_days = (case.completed_at - case.assigned_at).days
            total_completion_days += processing_days
            
            # REWARD: Quick completion (within 5 days)
            if processing_days <= 5:
                quick_completions += 1
                total_rewards += 5.0  # +5% reward for quick resolution
            
            # PENALTY: Slow completion (more than 10 days)
            elif processing_days > 10:
                slow_completions += 1
                days_over = processing_days - 10
                total_penalties += (days_over * 2.0)  # -2% per day over 10
        
        # PENALTY: Case was at risk at completion
        if case.sla_status == SLAStatus.AT_RISK:
            at_risk_cases += 1
            total_penalties += 5.0  # -5% penalty
        
        # PENALTY: Case was breached at completion
        if case.sla_status == SLAStatus.BREACHED:
            breached_cases += 1
            total_penalties += 5.0  # -5% penalty
    
    # Calculate average completion time
    avg_completion_days = total_completion_days / total_completed if total_completed > 0 else 0
    
    # PENALTY: Rejections (-5% each)
    total_rejections = int(dca.total_cases_rejected) if dca.total_cases_rejected is not None else 0
    if total_rejections > 0:
        total_penalties += (total_rejections * 5.0)
    
    # PENALTY: Delays (-3% each)
    total_delays = int(dca.total_delays) if dca.total_delays is not None else 0
    if total_delays > 0:
        total_penalties += (total_delays * 3.0)
    
    # Calculate final score: Base + Rewards - Penalties
    final_score = base_score + total_rewards - total_penalties
    
    # Cap score between 0 and 120 (allow exceeding 100% for exceptional performance)
    final_score = max(0.0, min(120.0, final_score))
    
    # Update DCA metrics (will be committed by caller)
    dca.avg_completion_time_days = round(avg_completion_days, 2)
    
    # Log calculation for debugging
    print(f"[Performance] DCA: {dca.name}")
    print(f"  Completed: {total_completed}, Quick: {quick_completions}, Slow: {slow_completions}")
    print(f"  At Risk: {at_risk_cases}, Breached: {breached_cases}")
    print(f"  Rejections: {total_rejections}, Delays: {total_delays}")
    print(f"  Rewards: +{total_rewards}%, Penalties: -{total_penalties}%")
    print(f"  Final Score: {round(final_score, 1)}%")
    
    return round(final_score, 1)


def update_active_case_count(dca: DCA, db: Session):
    """
    Update the active case count for a DCA.
    Completed cases should NOT be in active count.
    """
    active_count = db.query(Case).filter(
        Case.dca_id == dca.id,
        Case.status.in_([CaseStatus.OPEN, CaseStatus.IN_PROGRESS])
    ).count()
    
    dca.active_cases_count = active_count
