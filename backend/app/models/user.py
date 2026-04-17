from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.models.favorites import user_favorite_club, user_favorite_activity

# Represents a single user in our system
class User(Base, TimestampMixin):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Relationships
    # Links the user to the activities they joined (one-to-many)
    activities = relationship("UserActivity", back_populates="user", cascade="all, delete-orphan")
    # Links the user to the posts they created (one-to-many)
    community_posts = relationship("CommunityPost", back_populates="user", cascade="all, delete-orphan")
    # Links the user to their favorite clubs (many-to-many)
    favorite_clubs = relationship("Club", secondary=user_favorite_club, back_populates="favorited_by")
    # Links the user to their favorite activities (many-to-many)
    favorite_activities = relationship("Activity", secondary=user_favorite_activity, back_populates="favorited_by")
