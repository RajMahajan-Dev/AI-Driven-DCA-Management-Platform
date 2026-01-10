from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime

from ..database import get_db
from ..models.models import Case, DCA, User

router = APIRouter(prefix="/api/v1/customer", tags=["customer"])


class PaymentRequest(BaseModel):
    case_id: int
    amount: float


class ComplaintRequest(BaseModel):
    case_id: int
    complaint: str


class UpdateRequest(BaseModel):
    case_id: int
    update_info: str


@router.get("/cases")
async def get_customer_cases(email: str, db: Session = Depends(get_db)):
    """Get all cases for a customer by email"""
    cases = db.query(Case).filter(Case.customer_email == email).all()
    
    if not cases:
        raise HTTPException(status_code=404, detail="No cases found for this email")
    
    result = []
    for case in cases:
        result.append({
            "id": case.id,
            "case_id": case.case_id,
            "customer_name": case.customer_name,
            "customer_email": case.customer_email,
            "overdue_amount": case.overdue_amount,
            "status": case.status,
            "priority": case.priority,
        })
    
    return result


@router.get("/dashboard/{case_id}")
async def get_customer_dashboard(case_id: int, db: Session = Depends(get_db)):
    """Get detailed case information for customer dashboard"""
    case = db.query(Case).filter(Case.id == case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    dca_name = None
    if case.dca_id:
        dca = db.query(DCA).filter(DCA.id == case.dca_id).first()
        if dca:
            dca_name = dca.name
    
    return {
        "id": case.id,
        "case_id": case.case_id,
        "customer_name": case.customer_name,
        "customer_email": case.customer_email,
        "customer_phone": case.customer_phone,
        "customer_address": case.customer_address,
        "overdue_amount": case.overdue_amount,
        "status": case.status,
        "priority": case.priority,
        "ageing_days": case.ageing_days,
        "sla_due_date": case.sla_due_date.isoformat() if case.sla_due_date else None,
        "sla_status": case.sla_status,
        "dca_name": dca_name,
        "notes": case.notes,
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "customer_social_media_instagram": case.customer_social_media_instagram,
        "customer_social_media_facebook": case.customer_social_media_facebook,
        "customer_social_media_linkedin": case.customer_social_media_linkedin,
    }


@router.post("/payment")
async def submit_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    """Handle customer payment submission"""
    case = db.query(Case).filter(Case.id == payment.case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Add payment note to case
    payment_note = f"\n[Payment Request - {datetime.now().strftime('%Y-%m-%d %H:%M')}] Customer submitted payment of ${payment.amount:,.2f}"
    case.notes = (case.notes or "") + payment_note
    
    # If full amount paid, update status
    if payment.amount >= case.overdue_amount:
        case.status = "CLOSED"
        case.notes += " - Full payment received, case closed."
    
    db.commit()
    
    return {
        "success": True,
        "message": "Payment request submitted successfully",
        "case_id": case.case_id
    }


@router.post("/complaint")
async def register_complaint(complaint: ComplaintRequest, db: Session = Depends(get_db)):
    """Register a customer complaint"""
    case = db.query(Case).filter(Case.id == complaint.case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Add complaint to case notes
    complaint_note = f"\n[COMPLAINT - {datetime.now().strftime('%Y-%m-%d %H:%M')}]\n{complaint.complaint}"
    case.notes = (case.notes or "") + complaint_note
    
    db.commit()
    
    return {
        "success": True,
        "message": "Complaint registered successfully. Admin will review it.",
        "case_id": case.case_id
    }


@router.post("/update-request")
async def submit_update_request(update: UpdateRequest, db: Session = Depends(get_db)):
    """Submit customer information update request"""
    case = db.query(Case).filter(Case.id == update.case_id).first()
    
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Add update request to case notes for admin review
    update_note = f"\n[UPDATE REQUEST - {datetime.now().strftime('%Y-%m-%d %H:%M')}]\nCustomer requested update:\n{update.update_info}\n[Status: Pending Admin Approval]"
    case.notes = (case.notes or "") + update_note
    
    db.commit()
    
    return {
        "success": True,
        "message": "Update request submitted. Admin will review and approve changes.",
        "case_id": case.case_id
    }
