from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db
from app.models.models import Doctor, VerificationStatus
from app.config import settings
from pydantic import BaseModel
from app.auth import create_access_token, create_refresh_token  

router = APIRouter(prefix="/auth", tags=["Authentication"])


class GoogleAuthRequest(BaseModel):
    email: str


@router.post("/verify-google-auth")
def verify_google_auth(
    request: GoogleAuthRequest,
    db: Session = Depends(get_db),
    api_key: str = Header(None, alias="APIKEY"),
):
    """
    ✅ Verify Google Authentication (with JWT + Refresh token)
    Request body: { "email": "contact.digidr@gmail.com" }
    """

    if api_key != settings.STATIC_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )

    email = request.email
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is required"
        )

    try:

        doctor = db.query(Doctor).filter(Doctor.email == email).first()
        is_new_user = False

        if not doctor:
            
            doctor = Doctor(
                full_name="",
                email=email,
                hashed_password="google_auth_user",  
                is_verified=VerificationStatus.VERIFIED,
                created_at=datetime.utcnow()
            )
            db.add(doctor)
            db.commit()
            db.refresh(doctor)
            is_new_user = True


        token_data = {"sub": str(doctor.id), "email": doctor.email}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)


        user_info = {
            "id": doctor.id,
            "full_name": doctor.full_name,
            "email": doctor.email,
            "profile_photo": doctor.profile_photo,
            "is_verified": str(doctor.is_verified),
            "created_at": doctor.created_at.isoformat() if doctor.created_at else None,
            "updated_at": doctor.updated_at.isoformat() if doctor.updated_at else None,
            "new_user": is_new_user
        }


        return {
            "message": "Doctor authenticated successfully via Google",
            "status": status.HTTP_200_OK,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_info": user_info
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during Google authentication: {str(e)}"
        )
