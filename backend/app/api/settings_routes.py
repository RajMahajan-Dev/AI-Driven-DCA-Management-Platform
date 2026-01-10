from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.database import get_db
from app.models import Settings, User, RoleEnum
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/settings", tags=["Settings"])


class SettingsUpdate(BaseModel):
    # SLA Parameters
    p1_sla_days: Optional[int] = None
    p2_sla_days: Optional[int] = None
    p3_sla_days: Optional[int] = None
    
    # Performance Score Parameters
    delay_penalty_percent: Optional[float] = None
    breach_penalty_percent: Optional[float] = None
    processing_threshold_days: Optional[int] = None
    processing_penalty_per_day: Optional[float] = None
    rejection_penalty_percent: Optional[float] = None
    
    # Theme Settings
    theme_primary_color: Optional[str] = None
    theme_secondary_color: Optional[str] = None
    theme_mode: Optional[str] = None
    
    # Time/Timezone Settings
    timezone: Optional[str] = None
    date_format: Optional[str] = None
    time_format: Optional[str] = None
    
    # Feature Flags
    ai_assignment_enabled: Optional[bool] = None
    email_notifications_enabled: Optional[bool] = None
    sms_notifications_enabled: Optional[bool] = None


@router.get("")
def get_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get current platform settings."""
    settings = db.query(Settings).first()
    
    # Create default settings if none exist
    if not settings:
        settings = Settings()
        db.add(settings)
        db.commit()
        db.refresh(settings)
    
    return {
        "id": settings.id,
        # SLA Parameters
        "p1_sla_days": settings.p1_sla_days,
        "p2_sla_days": settings.p2_sla_days,
        "p3_sla_days": settings.p3_sla_days,
        # Performance Parameters
        "delay_penalty_percent": settings.delay_penalty_percent,
        "breach_penalty_percent": settings.breach_penalty_percent,
        "processing_threshold_days": settings.processing_threshold_days,
        "processing_penalty_per_day": settings.processing_penalty_per_day,
        "rejection_penalty_percent": settings.rejection_penalty_percent,
        # Theme
        "theme_primary_color": settings.theme_primary_color,
        "theme_secondary_color": settings.theme_secondary_color,
        "theme_mode": settings.theme_mode,
        # Time
        "timezone": settings.timezone,
        "date_format": settings.date_format,
        "time_format": settings.time_format,
        # Features
        "ai_assignment_enabled": settings.ai_assignment_enabled,
        "email_notifications_enabled": settings.email_notifications_enabled,
        "sms_notifications_enabled": settings.sms_notifications_enabled,
        "updated_at": settings.updated_at
    }


@router.put("")
def update_settings(
    update: SettingsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update platform settings (Admin only)."""
    # Check if user is admin
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    settings = db.query(Settings).first()
    
    # Create default settings if none exist
    if not settings:
        settings = Settings()
        db.add(settings)
    
    # Update fields that are provided
    update_data = update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    
    return {"message": "Settings updated successfully", "settings": get_settings(db, current_user)}


@router.post("/reset")
def reset_settings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reset settings to defaults (Admin only)."""
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    settings = db.query(Settings).first()
    
    if settings:
        db.delete(settings)
        db.commit()
    
    # Create new default settings
    settings = Settings()
    db.add(settings)
    db.commit()
    db.refresh(settings)
    
    return {"message": "Settings reset to defaults", "settings": get_settings(db, current_user)}
