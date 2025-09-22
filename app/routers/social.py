from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.models.models import Doctor
from app.models.social_account import SocialAccount
from app.schemas.social import SocialAccountResponse, OAuthUrlResponse
from app.routers.auth import get_current_doctor
import logging

router = APIRouter(prefix="/social", tags=["social"])
logger = logging.getLogger(__name__)

# Supported platforms
SUPPORTED_PLATFORMS = ["facebook", "instagram", "linkedin", "twitter", "youtube", "reddit", "quora"]


@router.get("/accounts", response_model=List[SocialAccountResponse])
async def list_social_accounts(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Get all connected social accounts for the logged-in doctor"""
    accounts = db.query(SocialAccount).filter(
        SocialAccount.doctor_id == current_doctor.id
    ).all()
    return accounts


@router.post("/connect/{platform}", response_model=OAuthUrlResponse)
async def generate_oauth_url(
    platform: str,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Generate OAuth authorization URL for the specified platform"""
    if platform not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Platform {platform} not supported. Supported platforms: {SUPPORTED_PLATFORMS}"
        )
    
    # For now, return a dummy URL - in production this would generate real OAuth URLs
    authorization_url = f"https://oauth.{platform}.com/authorize?client_id=dummy&redirect_uri=callback&scope=publish"
    
    logger.info(f"Generated OAuth URL for doctor {current_doctor.id} on platform {platform}")
    
    return OAuthUrlResponse(authorization_url=authorization_url)


@router.get("/callback/{platform}")
async def oauth_callback(
    platform: str,
    code: str = Query(..., description="OAuth authorization code"),
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Handle OAuth2 callback and save access token"""
    if platform not in SUPPORTED_PLATFORMS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Platform {platform} not supported"
        )
    
    # Check if account already exists
    existing_account = db.query(SocialAccount).filter(
        SocialAccount.doctor_id == current_doctor.id,
        SocialAccount.platform == platform
    ).first()
    
    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Social account for {platform} already connected"
        )
    
    # For now, create dummy token - in production this would exchange code for real tokens
    dummy_token = f"dummy_access_token_{platform}_{current_doctor.id}"
    
    # Create new social account
    new_account = SocialAccount(
        doctor_id=current_doctor.id,
        platform=platform,
        access_token=dummy_token,
        refresh_token=None,
        token_expires_at=None
    )
    
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    
    logger.info(f"Connected {platform} account for doctor {current_doctor.id}")
    
    return {"message": f"Successfully connected {platform} account", "account_id": new_account.id}


@router.delete("/accounts/{account_id}")
async def disconnect_social_account(
    account_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Disconnect a social media account"""
    account = db.query(SocialAccount).filter(
        SocialAccount.id == account_id,
        SocialAccount.doctor_id == current_doctor.id
    ).first()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social account not found or not owned by current doctor"
        )
    
    # Check if there are scheduled posts using this account
    from app.models.post import Post, PostStatus
    scheduled_posts = db.query(Post).filter(
        Post.social_account_id == account_id,
        Post.status == PostStatus.SCHEDULED
    ).count()
    
    if scheduled_posts > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot disconnect account with {scheduled_posts} scheduled posts. Cancel posts first."
        )
    
    platform = account.platform
    db.delete(account)
    db.commit()
    
    logger.info(f"Disconnected {platform} account {account_id} for doctor {current_doctor.id}")
    
    return {"message": f"Successfully disconnected {platform} account"}