from app.utils.publishers.base_publisher import BasePublisher
from app.models.post import Post
import logging

logger = logging.getLogger(__name__)


class FacebookPublisher(BasePublisher):
    """Facebook post publisher"""
    
    def __init__(self):
        super().__init__("Facebook")
    
    async def publish(self, post: Post) -> bool:
        """
        Publish a post to Facebook
        
        For now, this is a dummy implementation that just logs the action.
        In production, this would use the Facebook Graph API.
        """
        try:
            # Dummy implementation - in production, integrate with Facebook Graph API
            logger.info(f"Publishing post {post.id} for doctor {post.doctor_id} on Facebook...")
            logger.info(f"Content: {post.content[:100]}{'...' if len(post.content) > 100 else ''}")
            
            if post.media_url:
                logger.info(f"Media URL: {post.media_url}")
            
            # Simulate API call success
            self.log_success(post)
            return True
            
        except Exception as e:
            self.log_error(post, str(e))
            raise