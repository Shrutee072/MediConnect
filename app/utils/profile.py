from typing import Optional
from app.models.models import Doctor


def calculate_profile_completeness(doctor: Doctor) -> int:
    """
    Calculate the profile completeness percentage based on filled optional fields.
    Required fields (full_name, email, hashed_password) are not counted as they're always present.
    """
    # Define the optional fields that contribute to profile completeness
    optional_fields = [
        'clinic_name',
        'clinic_address', 
        'speciality_id',
        'sub_speciality_id',
        'years_of_experience',
        'medical_institute',
        'awards',
        'medical_council_regd_no',
        'profile_photo'
    ]
    
    filled_fields = 0
    total_fields = len(optional_fields)
    
    for field in optional_fields:
        value = getattr(doctor, field, None)
        
        # Handle different field types appropriately
        if field in ['speciality_id', 'sub_speciality_id', 'years_of_experience']:
            # For numeric fields, consider filled if not None and > 0
            if value is not None and value > 0:
                filled_fields += 1
        else:
            # For string fields, consider filled if not None and not empty string
            if value is not None and str(value).strip():
                filled_fields += 1
    
    # Calculate percentage
    completeness_percentage = int((filled_fields / total_fields) * 100) if total_fields > 0 else 100
    
    return completeness_percentage


def get_profile_completeness_tips(doctor: Doctor) -> list[str]:
    """
    Get tips for improving profile completeness based on missing fields.
    """
    tips = []
    
    clinic_name = getattr(doctor, 'clinic_name', None)
    if not clinic_name or not str(clinic_name).strip():
        tips.append("Add your clinic name to help patients find you")
    
    clinic_address = getattr(doctor, 'clinic_address', None)
    if not clinic_address or not str(clinic_address).strip():
        tips.append("Add your clinic address for better visibility")
    
    speciality_id = getattr(doctor, 'speciality_id', None)
    if speciality_id is None or speciality_id <= 0:
        tips.append("Select your medical speciality")
    
    sub_speciality_id = getattr(doctor, 'sub_speciality_id', None)
    if sub_speciality_id is None or sub_speciality_id <= 0:
        tips.append("Choose your sub-speciality for more specific expertise")
    
    years_of_experience = getattr(doctor, 'years_of_experience', None)
    if years_of_experience is None or years_of_experience <= 0:
        tips.append("Add your years of experience to build trust")
    
    medical_institute = getattr(doctor, 'medical_institute', None)
    if not medical_institute or not str(medical_institute).strip():
        tips.append("Mention your medical institute/university")
    
    awards = getattr(doctor, 'awards', None)
    if not awards or not str(awards).strip():
        tips.append("Add any awards or recognitions you've received")
    
    medical_council_regd_no = getattr(doctor, 'medical_council_regd_no', None)
    if not medical_council_regd_no or not str(medical_council_regd_no).strip():
        tips.append("Add your medical council registration number")
    
    profile_photo = getattr(doctor, 'profile_photo', None)
    if not profile_photo or not str(profile_photo).strip():
        tips.append("Upload a professional profile photo")
    
    return tips