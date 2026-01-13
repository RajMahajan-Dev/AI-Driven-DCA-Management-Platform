from pydantic_settings import BaseSettings
from typing import Optional, List


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
    
    # CORS Origins (comma-separated string for production)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:4567,http://localhost:8000"
    
    # AI/ML
    AI_MODEL_PATH: str = "app/ai/models/recovery_model.pkl"
    
    def get_cors_origins(self) -> List[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
