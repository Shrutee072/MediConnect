from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import SessionLocal
from app.models.post import Post, PostStatus
from app.utils.publishers.facebook_publisher import FacebookPublisher
from app.utils.publishers.instagram_publisher import InstagramPublisher
from app.utils.publishers.linkedin_publisher import LinkedInPublisher
from app.utils.publishers.twitter_publisher import TwitterPublisher
from app.utils.publishers.youtube_publisher import YouTubePublisher
from app.utils.publishers.reddit_publisher import RedditPublisher
from app.utils.publishers.quora_publisher import QuoraPublisher
import logging

logger = logging.getLogger(__name__)

# Publisher mapping
PUBLISHERS = {
    "facebook": FacebookPublisher(),
    "instagram": InstagramPublisher(),
    "linkedin": LinkedInPublisher(),
    "twitter": TwitterPublisher(),
    "youtube": YouTubePublisher(),
    "reddit": RedditPublisher(),
    "quora": QuoraPublisher(),
}

# Global scheduler instance
scheduler = AsyncIOScheduler()


async def check_due_posts():
    """Check for posts that are due to be published"""
    db: Session = SessionLocal()
    try:
        # Get all scheduled posts that are due
        due_posts = db.query(Post).filter(
            Post.status == PostStatus.SCHEDULED,
            Post.scheduled_at <= datetime.now()
        ).all()
        
        for post in due_posts:
            await publish_post(post, db)
            
    except Exception as e:
        logger.error(f"Error checking due posts: {str(e)}")
    finally:
        db.close()


async def publish_post(post: Post, db: Session):
    """Publish a single post using the appropriate publisher"""
    try:
        publisher = PUBLISHERS.get(post.platform)
        if not publisher:
            raise ValueError(f"No publisher found for platform: {post.platform}")
        
        logger.info(f"Publishing post {post.id} for doctor {post.doctor_id} on {post.platform}...")
        
        # Call the publisher
        await publisher.publish(post)
        
        # Update post status to published
        post.status = PostStatus.PUBLISHED
        post.error_message = None
        
        logger.info(f"Successfully published post {post.id} on {post.platform}")
        
    except Exception as e:
        # Update post status to failed
        post.status = PostStatus.FAILED
        post.error_message = str(e)
        
        logger.error(f"Failed to publish post {post.id} on {post.platform}: {str(e)}")
    
    finally:
        db.commit()


def start_scheduler():
    """Start the post scheduler"""
    if not scheduler.running:
        # Add job to check for due posts every minute
        scheduler.add_job(
            check_due_posts,
            trigger=IntervalTrigger(minutes=1),
            id="check_due_posts",
            name="Check for due posts",
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("Post scheduler started")


def stop_scheduler():
    """Stop the post scheduler"""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Post scheduler stopped")