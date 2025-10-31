import os
from typing import Optional

class Settings:
    # Database settings
    DATABASE_URL: Optional[str] = os.environ.get("DATABASE_URL")
    STATIC_API_KEY: Optional[str] = os.environ.get("STATIC_API_KEY")
    SECRET_KEY: Optional[str] = os.environ.get("SECRET_KEY")

    # JWT settings
    SECRET_KEY: str = os.environ.get("SESSION_SECRET")
    if not SECRET_KEY:
        raise ValueError("SESSION_SECRET environment variable is required for secure JWT operations")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OTP settings
    OTP_EXPIRE_MINUTES: int = 5
    OTP_LENGTH: int = 6
    
    # Application settings
    PROJECT_NAME: str = "Medical API"
    VERSION: str = "1.0.0"
    DEBUG: bool = os.environ.get("DEBUG", "false").lower() == "true"

settings = Settings()

