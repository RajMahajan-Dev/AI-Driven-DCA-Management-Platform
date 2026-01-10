from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.models import RoleEnum, CaseStatus, Priority, SLAStatus


# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: RoleEnum = RoleEnum.INTERNAL_USER


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# DCA Schemas
class DCABase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    performance_score: str = "TBD"
    max_capacity: int = Field(default=100, gt=0)
    is_active: bool = True
    min_debt_amount: float = Field(default=0.0, ge=0)
    max_debt_amount: float = Field(default=1000000.0, gt=0)
    website_url: Optional[str] = None
    document_url: Optional[str] = None


class DCACreate(DCABase):
    pass


class DCAUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    performance_score: Optional[str] = None
    max_capacity: Optional[int] = Field(default=None, gt=0)
    is_active: Optional[bool] = None
    min_debt_amount: Optional[float] = Field(default=None, ge=0)
    max_debt_amount: Optional[float] = Field(default=None, gt=0)
    website_url: Optional[str] = None
    document_url: Optional[str] = None
    total_cases_completed: Optional[int] = None
    total_cases_rejected: Optional[int] = None
    total_delays: Optional[int] = None
    avg_completion_time_days: Optional[float] = None


class DCAResponse(DCABase):
    id: int
    active_cases_count: int
    total_cases_completed: int
    total_cases_rejected: int
    total_delays: int
    avg_completion_time_days: float
    created_at: datetime
    
    class Config:
        from_attributes = True


# Case Schemas
class CaseBase(BaseModel):
    customer_name: str
    customer_email: Optional[EmailStr] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    customer_social_media_instagram: Optional[str] = None
    customer_social_media_facebook: Optional[str] = None
    customer_social_media_linkedin: Optional[str] = None
    customer_website_url: Optional[str] = None
    customer_document_url: Optional[str] = None
    family_info: Optional[str] = None
    overdue_amount: float = Field(gt=0)
    ageing_days: int = Field(ge=0)
    notes: Optional[str] = None


class CaseCreate(CaseBase):
    pass


class CaseUpdate(BaseModel):
    status: Optional[CaseStatus] = None
    notes: Optional[str] = None
    confirmation_received: Optional[bool] = None
    completed_at: Optional[datetime] = None


class CaseResponse(CaseBase):
    id: int
    case_id: str
    status: CaseStatus
    priority: Priority
    sla_due_date: Optional[datetime]
    sla_status: SLAStatus
    ai_recovery_score: float
    dca_id: Optional[int]
    allocation_reason: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    dca: Optional[DCAResponse] = None
    
    class Config:
        from_attributes = True


# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    case_id: Optional[int]
    action_type: str
    description: Optional[str]
    old_value: Optional[str]
    new_value: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStats(BaseModel):
    total_overdue_amount: float
    total_cases: int
    open_cases: int
    in_progress_cases: int
    closed_cases: int
    sla_breach_count: int
    at_risk_count: int
    total_dcas: int
    active_dcas: int
    # New fields for charts
    rejected_cases: int = 0
    pending_cases: int = 0
    pending_amount: float = 0
    recovered_amount: float = 0


# Escalation Schema
class EscalationRequest(BaseModel):
    reason: str
