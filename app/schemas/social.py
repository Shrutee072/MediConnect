from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.post import PostStatus


class SocialAccountBase(BaseModel):
    platform: str
    page_id: Optional[str] = None


class SocialAccountCreate(SocialAccountBase):
    access_token: str
    refresh_token: Optional[str] = None
    token_expires_at: Optional[datetime] = None


class SocialAccountResponse(SocialAccountBase):
    id: int
    doctor_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class PostBase(BaseModel):
    platform: str
    content: str
    media_url: Optional[str] = None
    scheduled_at: datetime


class PostCreate(PostBase):
    social_account_id: int


class PostUpdate(BaseModel):
    content: Optional[str] = None
    media_url: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class PostResponse(PostBase):
    id: int
    doctor_id: int
    social_account_id: int
    status: PostStatus
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class OAuthUrlResponse(BaseModel):
    authorization_url: str