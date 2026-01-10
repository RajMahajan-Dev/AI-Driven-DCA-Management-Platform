from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://dcauser:dcapass123@localhost:5432/dca_management"
    
    # JWT Authentication
    SECRET_KEY: str = "fedex-hackathon-secret-key-2026-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Application
    APP_NAME: str = "FedEx DCA Management Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # AI/ML
    AI_MODEL_PATH: str = "app/ai/models/recovery_model.pkl"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
