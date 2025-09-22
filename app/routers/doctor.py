from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

from app.db import get_db
from app.models.models import Doctor, MedicalSpeciality, MedicalSubSpeciality
from app.schemas.doctor import DoctorResponse, DoctorUpdate
from app.routers.auth import get_current_doctor

router = APIRouter(prefix="/doctor", tags=["Doctor Profile"])


@router.get("/profile", response_model=DoctorResponse)
async def get_doctor_profile(
    current_doctor: Annotated[Doctor, Depends(get_current_doctor)],
    db: Session = Depends(get_db)
):
    """Get the logged-in doctor's profile."""
    # Get speciality and sub-speciality names
    speciality_name = None
    sub_speciality_name = None
    
    if current_doctor.speciality_id is not None:
        speciality = db.query(MedicalSpeciality).filter(
            MedicalSpeciality.id == current_doctor.speciality_id
        ).first()
        if speciality:
            speciality_name = speciality.name
    
    if current_doctor.sub_speciality_id is not None:
        sub_speciality = db.query(MedicalSubSpeciality).filter(
            MedicalSubSpeciality.id == current_doctor.sub_speciality_id
        ).first()
        if sub_speciality:
            sub_speciality_name = sub_speciality.name
    
    # Create response with additional fields
    doctor_dict = DoctorResponse.model_validate(current_doctor).model_dump()
    doctor_dict['speciality_name'] = speciality_name
    doctor_dict['sub_speciality_name'] = sub_speciality_name
    
    return DoctorResponse(**doctor_dict)


@router.put("/profile", response_model=DoctorResponse)
async def update_doctor_profile(
    profile_data: DoctorUpdate,
    current_doctor: Annotated[Doctor, Depends(get_current_doctor)],
    db: Session = Depends(get_db)
):
    """Update the logged-in doctor's profile."""
    # Check if medical council registration number is already used by another doctor
    if profile_data.medical_council_regd_no:
        existing_reg = db.query(Doctor).filter(
            Doctor.medical_council_regd_no == profile_data.medical_council_regd_no,
            Doctor.id != current_doctor.id
        ).first()
        if existing_reg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Medical council registration number already exists"
            )
    
    # Validate speciality and sub-speciality if provided
    if profile_data.speciality_id:
        speciality = db.query(MedicalSpeciality).filter(
            MedicalSpeciality.id == profile_data.speciality_id
        ).first()
        if not speciality:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid speciality ID"
            )
    
    if profile_data.sub_speciality_id:
        sub_speciality = db.query(MedicalSubSpeciality).filter(
            MedicalSubSpeciality.id == profile_data.sub_speciality_id
        ).first()
        if not sub_speciality:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sub-speciality ID"
            )
        
        # Check if sub-speciality belongs to the selected speciality
        if profile_data.speciality_id and sub_speciality.speciality_id != profile_data.speciality_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sub-speciality does not belong to the selected speciality"
            )
    
    # Update doctor profile
    update_data = profile_data.model_dump(exclude_unset=True)
    if update_data:
        db.query(Doctor).filter(Doctor.id == current_doctor.id).update(update_data)
        db.commit()
        
        # Refresh the doctor object
        db.refresh(current_doctor)
    
    # Get updated profile with speciality names
    return await get_doctor_profile(current_doctor, db)