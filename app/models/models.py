from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Enum, func
from sqlalchemy.orm import relationship
import enum
from app.db import Base


class VerificationStatus(enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"


class MedicalSpeciality(Base):
    __tablename__ = "medical_specialities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    sub_specialities = relationship("MedicalSubSpeciality", back_populates="speciality")
    doctors = relationship("Doctor", back_populates="speciality")


class MedicalSubSpeciality(Base):
    __tablename__ = "medical_sub_specialities"
    
    id = Column(Integer, primary_key=True, index=True)
    speciality_id = Column(Integer, ForeignKey("medical_specialities.id"), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    speciality = relationship("MedicalSpeciality", back_populates="sub_specialities")
    doctors = relationship("Doctor", back_populates="sub_speciality")


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(200), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=True)
    phone_number = Column(String(20))  # WhatsApp contact number
    clinic_name = Column(String(200))
    clinic_address = Column(Text)
    speciality_id = Column(Integer, ForeignKey("medical_specialities.id"))
    sub_speciality_id = Column(Integer, ForeignKey("medical_sub_specialities.id"))
    years_of_experience = Column(Integer)
    qualification = Column(String(500))  # Professional qualifications
    medical_institute = Column(String(300))
    awards = Column(Text)
    medical_council_regd_no = Column(String(50), unique=True)
    profile_photo = Column(String(500))  # URL or file path
    professional_bio = Column(Text)  # Professional bio/description
    is_verified = Column(Enum(VerificationStatus), default=VerificationStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    speciality = relationship("MedicalSpeciality", back_populates="doctors")
    sub_speciality = relationship("MedicalSubSpeciality", back_populates="doctors")
    social_accounts = relationship("SocialAccount", back_populates="doctor")
    posts = relationship("Post", back_populates="doctor")


class OTPVerification(Base):
    __tablename__ = "otp_verifications"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    otp_code = Column(String(6), nullable=False)
    purpose = Column(String(20), nullable=False)  # registration, login, reset_password
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())



    



# class PostStatus(enum.Enum):
#     DRAFT = "DRAFT"
#     SCHEDULED = "SCHEDULED"
#     POSTED = "POSTED"
#     FAILED = "FAILED"


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, index=True)
#     doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
#     social_account_id = Column(Integer, ForeignKey("social_accounts.id"), nullable=True)
#     platform = Column(String(50), nullable=False)
#     content = Column(Text, nullable=True)
#     media_url = Column(String(500), nullable=True)
#     scheduled_at = Column(DateTime(timezone=True), nullable=True)
#     status = Column(Enum(PostStatus), default=PostStatus.DRAFT)
#     error_message = Column(Text, nullable=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())

#     # Relationships
#     doctor = relationship("Doctor", back_populates="posts")
