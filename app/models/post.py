from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
import enum


class PostStatus(enum.Enum):
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"


class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    social_account_id = Column(Integer, ForeignKey("social_accounts.id", ondelete="CASCADE"), nullable=False)
    platform = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    media_url = Column(String(500), nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(PostStatus), default=PostStatus.SCHEDULED)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    doctor = relationship("Doctor", back_populates="posts")
    social_account = relationship("SocialAccount", back_populates="posts")