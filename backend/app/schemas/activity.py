import datetime
from pydantic import BaseModel, model_validator
from typing import Optional, List
from enum import Enum
from app.schemas.common import PaginationMeta
from app.schemas.club import ClubSummary
from app.schemas.user import UserSummary

class ActivityCategory(str, Enum):
    sports = "sports"
    club = "club"
    workshop = "workshop"
    social = "social"
    academic = "academic"
    other = "other"

class RegistrationStatus(str, Enum):
    joined = "joined"
    left = "left"
    cancelled = "cancelled"

class ActivityBase(BaseModel):
    activity_title: str
    activity_description: str
    activity_date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    activity_location: str
    max_slots: int
    activity_category: str
    image_path: Optional[str] = None
    club_id: int

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    activity_title: Optional[str] = None
    activity_description: Optional[str] = None
    activity_date: Optional[datetime.date] = None
    start_time: Optional[datetime.time] = None
    end_time: Optional[datetime.time] = None
    activity_location: Optional[str] = None
    max_slots: Optional[int] = None
    activity_category: Optional[str] = None
    image_path: Optional[str] = None
    club_id: Optional[int] = None

class Registration(BaseModel):
    registration_id: int
    registration_status: RegistrationStatus
    joined_at: datetime.datetime
    user_id: int
    activity_id: int
    user: Optional[UserSummary] = None

    class Config:
        from_attributes = True

class ActivitySummary(ActivityBase):
    activity_id: int
    club: Optional[ClubSummary] = None
    joined_count: int = 0
    available_slots: int = 0
    is_favorited: bool = False
    my_registration_status: Optional[RegistrationStatus] = None

    @model_validator(mode='before')
    @classmethod
    def populate_dates(cls, data):
        # Convert DB start_date/end_date into activity_date, start_time, end_time
        if hasattr(data, "start_date") and hasattr(data, "end_date"):
            start = data.start_date
            end = data.end_date
            if start:
                data.activity_date = start.date()
                data.start_time = start.time()
            if end:
                data.end_time = end.time()
        elif isinstance(data, dict):
            start = data.get("start_date")
            end = data.get("end_date")
            if isinstance(start, datetime.datetime):
                data["activity_date"] = start.date()
                data["start_time"] = start.time()
            if isinstance(end, datetime.datetime):
                data["end_time"] = end.time()
        return data

    class Config:
        from_attributes = True

class ActivityDetail(ActivitySummary):
    pass

class JoinActivityRequest(BaseModel):
    status: RegistrationStatus = RegistrationStatus.joined

class ActivityListResponse(BaseModel):
    items: List[ActivitySummary]
    meta: PaginationMeta

class RegistrationListResponse(BaseModel):
    items: List[Registration]
