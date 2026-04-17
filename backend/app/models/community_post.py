from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin

# Represents a forum post made by a user
class CommunityPost(Base, TimestampMixin):
    __tablename__ = 'community_posts'

    community_post_id = Column(Integer, primary_key=True, index=True)
    community_post_title = Column(String(50), nullable=False)
    community_post_description = Column(Text, nullable=False)
    community_post_category = Column(String(20), nullable=False)
    community_post_keywords = Column(String(255), nullable=True)
    
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    club_id = Column(Integer, ForeignKey('clubs.club_id', ondelete='SET NULL'), nullable=True)

    # Relationships
    # Links the post to the user who wrote it (many-to-one)
    user = relationship("User", back_populates="community_posts")
    # Links the post to an optional club it discusses (many-to-one)
    club = relationship("Club", back_populates="community_posts")
