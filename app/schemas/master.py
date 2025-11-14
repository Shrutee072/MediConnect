from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MedicalSpecialityBase(BaseModel):
    name: str


class MedicalSpecialityCreate(MedicalSpecialityBase):
    pass


class MedicalSpecialityResponse(MedicalSpecialityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MedicalSubSpecialityBase(BaseModel):
    speciality_id: int
    name: str


class MedicalSubSpecialityCreate(MedicalSubSpecialityBase):
    pass


class MedicalSubSpecialityResponse(MedicalSubSpecialityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    speciality_name: Optional[str] = None

    class Config:
        from_attributes = True


class SpecialitiesListResponse(BaseModel):
    specialities: List[MedicalSpecialityResponse]
    total: int


class SubSpecialitiesListResponse(BaseModel):
    sub_specialities: List[MedicalSubSpecialityResponse]
    total: int
    speciality_id: Optional[int] = None



class CreateSpeciality(BaseModel):
    name: str

class CreateSubSpeciality(BaseModel):
    name: str
    speciality_id: int
