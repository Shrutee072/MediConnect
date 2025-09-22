from app.utils.publishers.base_publisher import BasePublisher
from app.models.post import Post
import logging

logger = logging.getLogger(__name__)


class InstagramPublisher(BasePublisher):
    """Instagram post publisher"""
    
    def __init__(self):
        super().__init__("Instagram")
    
    async def publish(self, post: Post) -> bool:
        """
        Publish a post to Instagram
        
        For now, this is a dummy implementation that just logs the action.
        In production, this would use the Instagram Basic Display API.
        """
        try:
            # Dummy implementation - in production, integrate with Instagram API
            logger.info(f"Publishing post {post.id} for doctor {post.doctor_id} on Instagram...")
            logger.info(f"Content: {post.content[:100]}{'...' if len(post.content) > 100 else ''}")
            
            if post.media_url:
                logger.info(f"Media URL: {post.media_url}")
            
            # Simulate API call success
            self.log_success(post)
            return True
            
        except Exception as e:
            self.log_error(post, str(e))
            raise