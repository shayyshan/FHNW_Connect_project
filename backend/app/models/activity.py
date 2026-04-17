from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.mixins import TimestampMixin
from app.models.favorites import user_favorite_activity

# Represents a specific event or activity created by a club
class Activity(Base, TimestampMixin):
    __tablename__ = 'activities'

    activity_id = Column(Integer, primary_key=True, index=True)
    activity_title = Column(String(100), nullable=False)
    activity_description = Column(Text, nullable=True)
    activity_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    activity_location = Column(String(100), nullable=True)
    max_slots = Column(Integer, nullable=True)
    activity_category = Column(Text, nullable=True)
    image_path = Column(String(255), nullable=True)
    
    club_id = Column(Integer, ForeignKey('clubs.club_id', ondelete='CASCADE'), nullable=False)

    # Relationships
    # Links back to the club that created this activity (many-to-one)
    club = relationship("Club", back_populates="activities")
    # Links the activity to the users who joined it (one-to-many connection to the junction table)
    participants = relationship("UserActivity", back_populates="activity", cascade="all, delete-orphan")
    # Links the activity to the users who favorited it (many-to-many)
    favorited_by = relationship("User", secondary=user_favorite_activity, back_populates="favorite_activities")
