from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class DoctorBase(BaseModel):
    full_name: str
    email: EmailStr
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    speciality_id: Optional[int] = None
    sub_speciality_id: Optional[int] = None
    years_of_experience: Optional[int] = None
    medical_institute: Optional[str] = None
    awards: Optional[str] = None
    medical_council_regd_no: Optional[str] = None
    profile_photo: Optional[str] = None


class DoctorCreate(DoctorBase):
    password: str


class DoctorUpdate(BaseModel):
    full_name: Optional[str] = None
    clinic_name: Optional[str] = None
    clinic_address: Optional[str] = None
    speciality_id: Optional[int] = None
    sub_speciality_id: Optional[int] = None
    years_of_experience: Optional[int] = None
    medical_institute: Optional[str] = None
    awards: Optional[str] = None
    medical_council_regd_no: Optional[str] = None
    profile_photo: Optional[str] = None


class DoctorResponse(DoctorBase):
    id: int
    is_verified: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Related data
    speciality_name: Optional[str] = None
    sub_speciality_name: Optional[str] = None
    
    # Profile completeness
    completeness_percentage: int
    completeness_tips: Optional[List[str]] = None

    class Config:
        from_attributes = True