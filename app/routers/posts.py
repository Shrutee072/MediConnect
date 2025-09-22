from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from app.db import get_db
from app.models.models import Doctor
from app.models.social_account import SocialAccount
from app.models.post import Post, PostStatus
from app.schemas.social import PostCreate, PostUpdate, PostResponse
from app.routers.auth import get_current_doctor
import logging

router = APIRouter(prefix="/posts", tags=["posts"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=PostResponse)
async def create_scheduled_post(
    post_data: PostCreate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Create a scheduled post"""
    # Verify the social account belongs to the current doctor
    social_account = db.query(SocialAccount).filter(
        SocialAccount.id == post_data.social_account_id,
        SocialAccount.doctor_id == current_doctor.id
    ).first()
    
    if not social_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Social account not found or not owned by current doctor"
        )
    
    # Check if scheduled time is in the future
    if post_data.scheduled_at <= datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scheduled time must be in the future"
        )
    
    # Create new post
    new_post = Post(
        doctor_id=current_doctor.id,
        social_account_id=post_data.social_account_id,
        platform=social_account.platform,
        content=post_data.content,
        media_url=post_data.media_url,
        scheduled_at=post_data.scheduled_at,
        status=PostStatus.SCHEDULED
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    logger.info(f"Created scheduled post {new_post.id} for doctor {current_doctor.id} on {social_account.platform}")
    
    return new_post


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """List all posts for the logged-in doctor"""
    posts = db.query(Post).filter(
        Post.doctor_id == current_doctor.id
    ).order_by(Post.created_at.desc()).all()
    
    return posts


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    post_update: PostUpdate,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Update a scheduled post (only if status is SCHEDULED)"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.doctor_id == current_doctor.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or not owned by current doctor"
        )
    
    if post.status != PostStatus.SCHEDULED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only update scheduled posts"
        )
    
    # Update fields
    update_data = post_update.model_dump(exclude_unset=True)
    
    # Validate scheduled_at if provided
    if "scheduled_at" in update_data:
        if update_data["scheduled_at"] <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Scheduled time must be in the future"
            )
    
    for field, value in update_data.items():
        setattr(post, field, value)
    
    db.commit()
    db.refresh(post)
    
    logger.info(f"Updated post {post_id} for doctor {current_doctor.id}")
    
    return post


@router.delete("/{post_id}")
async def cancel_post(
    post_id: int,
    current_doctor: Doctor = Depends(get_current_doctor),
    db: Session = Depends(get_db)
):
    """Cancel a scheduled post"""
    post = db.query(Post).filter(
        Post.id == post_id,
        Post.doctor_id == current_doctor.id
    ).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or not owned by current doctor"
        )
    
    if post.status != PostStatus.SCHEDULED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only cancel scheduled posts"
        )
    
    db.delete(post)
    db.commit()
    
    logger.info(f"Cancelled post {post_id} for doctor {current_doctor.id}")
    
    return {"message": "Post cancelled successfully"}