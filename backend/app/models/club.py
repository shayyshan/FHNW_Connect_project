from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.models.favorites import user_favorite_club

# Represents a student club in our system
class Club(Base, TimestampMixin):
    __tablename__ = 'clubs'

    club_id = Column(Integer, primary_key=True, index=True)
    club_name = Column(String(100), unique=True, index=True, nullable=False)
    club_description = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=True)

    # Relationships
    # Links the club to all the activities it hosts (one-to-many)
    activities = relationship("Activity", back_populates="club", cascade="all, delete-orphan")
    # Links the club to posts written about it (one-to-many)
    community_posts = relationship("CommunityPost", back_populates="club")
    # Links the club to all the users who added it to their favorites (many-to-many)
    favorited_by = relationship("User", secondary=user_favorite_club, back_populates="favorite_clubs")
