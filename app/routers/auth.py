from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

from app.db import get_db
from app.models.models import Doctor, VerificationStatus
from app.schemas.auth import (
    DoctorRegisterRequest, OTPVerificationRequest, LoginRequest, 
    TokenResponse, OTPResponse
)
from app.utils.jwt import (
    verify_password, get_password_hash, create_access_token, 
    get_current_user_id
)
from app.utils.otp import create_otp, verify_otp, send_otp_email
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


def get_current_doctor(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db)
):
    """Get the current authenticated doctor."""
    token = credentials.credentials
    user_id = get_current_user_id(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    doctor = db.query(Doctor).filter(Doctor.id == user_id).first()
    if doctor is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Doctor not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return doctor


@router.post("/register", response_model=OTPResponse)
async def register_doctor(
    doctor_data: DoctorRegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new doctor and send OTP for verification."""
    # Check if doctor already exists
    existing_doctor = db.query(Doctor).filter(Doctor.email == doctor_data.email).first()
    if existing_doctor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Doctor with this email already exists"
        )
    
    # Check if medical council registration number is already used
    if doctor_data.medical_council_regd_no:
        existing_reg = db.query(Doctor).filter(
            Doctor.medical_council_regd_no == doctor_data.medical_council_regd_no
        ).first()
        if existing_reg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Medical council registration number already exists"
            )
    
    # Create doctor record
    hashed_password = get_password_hash(doctor_data.password)
    new_doctor = Doctor(
        full_name=doctor_data.full_name,
        email=doctor_data.email,
        hashed_password=hashed_password,
        clinic_name=doctor_data.clinic_name,
        clinic_address=doctor_data.clinic_address,
        speciality_id=doctor_data.speciality_id,
        sub_speciality_id=doctor_data.sub_speciality_id,
        years_of_experience=doctor_data.years_of_experience,
        medical_institute=doctor_data.medical_institute,
        awards=doctor_data.awards,
        medical_council_regd_no=doctor_data.medical_council_regd_no,
        profile_photo=doctor_data.profile_photo,
        is_verified=VerificationStatus.PENDING
    )
    
    db.add(new_doctor)
    db.commit()
    
    # Generate and send OTP
    otp_code, expires_at = create_otp(db, doctor_data.email, "registration")
    send_otp_email(doctor_data.email, otp_code, "registration")
    
    return OTPResponse(
        message="Registration successful. Please verify your email with the OTP sent to your email address.",
        email=doctor_data.email,
        expires_in_minutes=settings.OTP_EXPIRE_MINUTES
    )


@router.post("/verify-registration", response_model=TokenResponse)
async def verify_registration(
    verification_data: OTPVerificationRequest,
    db: Session = Depends(get_db)
):
    """Verify OTP and complete registration."""
    # Verify OTP
    if not verify_otp(db, verification_data.email, verification_data.otp_code, "registration"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Get the doctor
    doctor = db.query(Doctor).filter(Doctor.email == verification_data.email).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Mark doctor as verified
    db.query(Doctor).filter(Doctor.id == doctor.id).update({
        "is_verified": VerificationStatus.VERIFIED
    })
    db.commit()
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(doctor.id)}, expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.post("/login", response_model=OTPResponse)
async def login_request(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """Request login and send OTP."""
    # Check if doctor exists and password is correct
    doctor = db.query(Doctor).filter(Doctor.email == login_data.email).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(login_data.password, str(doctor.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if doctor is verified
    if doctor.is_verified != VerificationStatus.VERIFIED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account not verified. Please complete email verification first."
        )
    
    # Generate and send OTP
    otp_code, expires_at = create_otp(db, login_data.email, "login")
    send_otp_email(login_data.email, otp_code, "login")
    
    return OTPResponse(
        message="OTP sent to your email address. Please verify to complete login.",
        email=login_data.email,
        expires_in_minutes=settings.OTP_EXPIRE_MINUTES
    )


@router.post("/verify-login", response_model=TokenResponse)
async def verify_login(
    verification_data: OTPVerificationRequest,
    db: Session = Depends(get_db)
):
    """Verify OTP and complete login."""
    # Verify OTP
    if not verify_otp(db, verification_data.email, verification_data.otp_code, "login"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Get the doctor
    doctor = db.query(Doctor).filter(Doctor.email == verification_data.email).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Doctor not found"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(doctor.id)}, expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )