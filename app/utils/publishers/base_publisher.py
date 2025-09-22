from abc import ABC, abstractmethod
from app.models.post import Post
import logging

logger = logging.getLogger(__name__)


class BasePublisher(ABC):
    """Base class for all social media publishers"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
    
    @abstractmethod
    async def publish(self, post: Post) -> bool:
        """
        Publish a post to the social media platform
        
        Args:
            post: The Post object containing content and metadata
            
        Returns:
            bool: True if successful, False otherwise
            
        Raises:
            Exception: If publishing fails
        """
        pass
    
    def log_success(self, post: Post):
        """Log successful publication"""
        logger.info(f"Published post {post.id} for doctor {post.doctor_id} on {self.platform_name}")
    
    def log_error(self, post: Post, error: str):
        """Log publication error"""
        logger.error(f"Failed to publish post {post.id} on {self.platform_name}: {error}")