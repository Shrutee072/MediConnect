import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from app.models.models import OTPVerification
from app.config import settings


def generate_otp() -> str:
    """Generate a random OTP code."""
    return ''.join(random.choices(string.digits, k=settings.OTP_LENGTH))


def create_otp(db: Session, email: str, purpose: str) -> tuple[str, datetime]:
    """Create and store an OTP for email verification."""
    # Clean up any existing OTPs for this email and purpose
    db.query(OTPVerification).filter(
        OTPVerification.email == email,
        OTPVerification.purpose == purpose
    ).delete()
    
    # Generate new OTP
    otp_code = generate_otp()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    
    # Store OTP in database
    otp_record = OTPVerification(
        email=email,
        otp_code=otp_code,
        purpose=purpose,
        expires_at=expires_at
    )
    db.add(otp_record)
    db.commit()
    
    return otp_code, expires_at


def verify_otp(db: Session, email: str, otp_code: str, purpose: str) -> bool:
    """Verify an OTP code."""
    otp_record = db.query(OTPVerification).filter(
        OTPVerification.email == email,
        OTPVerification.otp_code == otp_code,
        OTPVerification.purpose == purpose,
        OTPVerification.is_used == False,
        OTPVerification.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not otp_record:
        return False
    
    # Mark OTP as used
    db.query(OTPVerification).filter(
        OTPVerification.id == otp_record.id
    ).update({"is_used": True})
    db.commit()
    
    return True


def send_otp_email(email: str, otp_code: str, purpose: str) -> dict:
    """Simulate sending OTP via email (for demo purposes)."""
    # In a real application, you would integrate with an email service
    # For this demo, we'll just return a success message
    return {
        "success": True,
        "message": f"OTP {otp_code} sent to {email} for {purpose}",
        "email": email,
        "otp_code": otp_code  # Remove this in production!
    }