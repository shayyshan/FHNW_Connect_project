from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base

# Represents a user joining an activity (many-to-many connection between User and Activity)
class UserActivity(Base):
    __tablename__ = 'user_activities'

    registration_id = Column(Integer, primary_key=True, index=True)
    registration_status = Column(String(20), nullable=False, default="joined")
    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    activity_id = Column(Integer, ForeignKey('activities.activity_id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'activity_id', name='uq_user_activity_registration'),
    )

    # Relationships
    # Links back to the user who joined (many-to-one)
    user = relationship("User", back_populates="activities")
    # Links back to the activity they joined (many-to-one)
    activity = relationship("Activity", back_populates="participants")
