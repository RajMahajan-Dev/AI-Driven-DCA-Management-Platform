"""
Settings Model for configurable platform parameters
"""
from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.database import Base


class Settings(Base):
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # SLA Parameters (in days)
    p1_sla_days = Column(Integer, default=3)
    p2_sla_days = Column(Integer, default=7)
    p3_sla_days = Column(Integer, default=14)
    
    # Performance Score Parameters
    delay_penalty_percent = Column(Float, default=3.0)  # Penalty for each delay
    breach_penalty_percent = Column(Float, default=5.0)  # Penalty for breached/at-risk cases
    processing_threshold_days = Column(Integer, default=10)  # Days before penalty applies
    processing_penalty_per_day = Column(Float, default=2.0)  # Penalty per day over threshold
    rejection_penalty_percent = Column(Float, default=5.0)  # Penalty for each rejection
    
    # Theme Settings
    theme_primary_color = Column(String, default="#6366f1")  # Indigo
    theme_secondary_color = Column(String, default="#8b5cf6")  # Purple
    theme_mode = Column(String, default="light")  # light or dark
    
    # Time/Timezone Settings
    timezone = Column(String, default="UTC")
    date_format = Column(String, default="YYYY-MM-DD")
    time_format = Column(String, default="24h")  # 12h or 24h
    
    # Feature Flags
    ai_assignment_enabled = Column(Boolean, default=True)
    email_notifications_enabled = Column(Boolean, default=True)
    sms_notifications_enabled = Column(Boolean, default=False)
    
    # Updated timestamp
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
