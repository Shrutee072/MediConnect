from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db import get_db
from app.models.models import MedicalSpeciality, MedicalSubSpeciality
from app.schemas.master import (
    SpecialitiesListResponse, SubSpecialitiesListResponse,
    MedicalSpecialityResponse, MedicalSubSpecialityResponse
)

router = APIRouter(prefix="/master", tags=["Master Data"])


@router.get("/specialities", response_model=SpecialitiesListResponse)
async def get_specialities(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Number of records to return")
):
    """Get list of all medical specialities."""
    specialities = db.query(MedicalSpeciality).offset(skip).limit(limit).all()
    total = db.query(MedicalSpeciality).count()
    
    specialities_data = [
        MedicalSpecialityResponse.model_validate(speciality) 
        for speciality in specialities
    ]
    
    return SpecialitiesListResponse(
        specialities=specialities_data,
        total=total
    )


@router.get("/sub-specialities", response_model=SubSpecialitiesListResponse)
async def get_sub_specialities(
    db: Session = Depends(get_db),
    speciality_id: Optional[int] = Query(None, description="Filter by speciality ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=500, description="Number of records to return")
):
    """Get list of medical sub-specialities, optionally filtered by speciality."""
    query = db.query(MedicalSubSpeciality)
    
    if speciality_id:
        query = query.filter(MedicalSubSpeciality.speciality_id == speciality_id)
    
    sub_specialities = query.offset(skip).limit(limit).all()
    total = query.count()
    
    # Prepare response data with speciality names
    sub_specialities_data = []
    for sub_speciality in sub_specialities:
        sub_speciality_data = MedicalSubSpecialityResponse.model_validate(sub_speciality)
        
        # Get speciality name
        if sub_speciality.speciality:
            sub_speciality_data.speciality_name = sub_speciality.speciality.name
        
        sub_specialities_data.append(sub_speciality_data)
    
    return SubSpecialitiesListResponse(
        sub_specialities=sub_specialities_data,
        total=total,
        speciality_id=speciality_id
    )