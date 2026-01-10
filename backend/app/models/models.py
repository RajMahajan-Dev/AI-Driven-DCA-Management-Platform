from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    INTERNAL_USER = "internal_user"


class CaseStatus(str, enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"


class Priority(str, enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class SLAStatus(str, enum.Enum):
    ON_TRACK = "On Track"
    AT_RISK = "At Risk"
    BREACHED = "Breached"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.INTERNAL_USER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")


class DCA(Base):
    __tablename__ = "dcas"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)
    performance_score = Column(String, default="TBD")  # TBD or 0-100
    active_cases_count = Column(Integer, default=0)
    max_capacity = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    
    # Performance metrics
    total_cases_completed = Column(Integer, default=0)
    total_cases_rejected = Column(Integer, default=0)
    total_delays = Column(Integer, default=0)
    avg_completion_time_days = Column(Float, default=0.0)
    
    # Debt collection range
    min_debt_amount = Column(Float, default=0.0)
    max_debt_amount = Column(Float, default=1000000.0)
    
    # Additional data sources
    website_url = Column(String, nullable=True)
    document_url = Column(String, nullable=True)  # PDF or other docs
    scraped_data = Column(Text, nullable=True)  # JSON data from scraping
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    cases = relationship("Case", back_populates="dca")


class Case(Base):
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String)
    customer_phone = Column(String)
    overdue_amount = Column(Float, nullable=False)
    ageing_days = Column(Integer, nullable=False)
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN)
    priority = Column(Enum(Priority), default=Priority.P3)
    sla_due_date = Column(DateTime(timezone=True))
    sla_status = Column(Enum(SLAStatus), default=SLAStatus.ON_TRACK)
    
    # Customer additional data
    customer_address = Column(Text, nullable=True)
    customer_social_media_instagram = Column(String, nullable=True)
    customer_social_media_facebook = Column(String, nullable=True)
    customer_social_media_linkedin = Column(String, nullable=True)
    customer_website_url = Column(String, nullable=True)
    customer_document_url = Column(String, nullable=True)
    scraped_customer_data = Column(Text, nullable=True)  # JSON data
    family_info = Column(Text, nullable=True)
    
    # AI/ML fields
    ai_recovery_score = Column(Float, default=0.0)  # 0-1
    
    # DCA assignment
    dca_id = Column(Integer, ForeignKey("dcas.id"), nullable=True)
    allocation_reason = Column(Text)
    assigned_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    confirmation_received = Column(Boolean, default=False)
    
    # Metadata
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    dca = relationship("DCA", back_populates="cases")
    audit_logs = relationship("AuditLog", back_populates="case")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)
    action_type = Column(String, nullable=False)  # e.g., "CREATE_CASE", "UPDATE_STATUS", etc.
    description = Column(Text)
    old_value = Column(Text)
    new_value = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    case = relationship("Case", back_populates="audit_logs")
