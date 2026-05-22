from pydantic import BaseModel
from typing import List
from app.schemas.activity import ActivitySummary
from app.schemas.club import ClubSummary

class DashboardResponse(BaseModel):
    calendar_items: List[ActivitySummary]
    upcoming_activities: List[ActivitySummary]
    favorite_clubs: List[ClubSummary]
    favorite_activities: List[ActivitySummary]

    class Config:
        from_attributes = True
