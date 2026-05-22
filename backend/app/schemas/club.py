from pydantic import BaseModel
from typing import Optional, List
from app.schemas.common import PaginationMeta

class ClubBase(BaseModel):
    club_name: str
    club_description: Optional[str] = None
    image_path: Optional[str] = None

class ClubCreate(ClubBase):
    pass

class ClubUpdate(BaseModel):
    club_name: Optional[str] = None
    club_description: Optional[str] = None
    image_path: Optional[str] = None

class ClubSummary(ClubBase):
    club_id: int
    is_favorited: Optional[bool] = False

    class Config:
        from_attributes = True

class ClubDetail(ClubSummary):
    upcoming_activities_count: Optional[int] = 0

    class Config:
        from_attributes = True

class ClubListResponse(BaseModel):
    items: List[ClubSummary]
    meta: PaginationMeta
