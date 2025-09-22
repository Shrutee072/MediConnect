from pydantic import BaseModel, EmailStr
from typing import Optional


class DoctorRegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    speciality_id: Optional[int] = None
    sub_speciality_id: Optional[int] = None
    years_of_experience: Optional[int] = None
    qualification: Optional[str] = None
    medical_institute: Optional[str] = None
    awards: Optional[str] = None
    medical_council_regd_no: Optional[str] = None
    profile_photo: Optional[str] = None
    professional_bio: Optional[str] = None


class OTPVerificationRequest(BaseModel):
    email: EmailStr
    otp_code: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class OTPResponse(BaseModel):
    message: str
    email: str
    expires_in_minutes: int