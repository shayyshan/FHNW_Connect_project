from pydantic import BaseModel, model_validator
from typing import Optional, List
import datetime
from app.schemas.common import PaginationMeta
from app.schemas.user import UserSummary
from app.schemas.club import ClubSummary

class CommunityPostBase(BaseModel):
    community_post_title: str
    community_post_description: str
    community_post_category: str
    community_post_keywords: Optional[List[str]] = None
    club_id: Optional[int] = None

class CommunityPostCreate(CommunityPostBase):
    pass

class CommunityPostUpdate(BaseModel):
    community_post_title: Optional[str] = None
    community_post_description: Optional[str] = None
    community_post_category: Optional[str] = None
    community_post_keywords: Optional[List[str]] = None
    club_id: Optional[int] = None

class CommunityPost(CommunityPostBase):
    community_post_id: int
    user_id: int
    author: Optional[UserSummary] = None
    club: Optional[ClubSummary] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    @model_validator(mode='before')
    @classmethod
    def process_keywords_and_relations(cls, data):
        # Convert DB string "a,b,c" to list ["a", "b", "c"]
        if hasattr(data, "community_post_keywords"):
            kws = data.community_post_keywords
            if isinstance(kws, str) and kws:
                data.community_post_keywords = [k.strip() for k in kws.split(",") if k.strip()]
            elif not kws:
                data.community_post_keywords = []
        elif isinstance(data, dict):
            kws = data.get("community_post_keywords")
            if isinstance(kws, str) and kws:
                data["community_post_keywords"] = [k.strip() for k in kws.split(",") if k.strip()]
            elif not kws:
                data["community_post_keywords"] = []
        
        # Map user relation to author name in OpenAPI
        if hasattr(data, "user") and data.user:
            data.author = data.user
        elif isinstance(data, dict) and "user" in data:
            data["author"] = data["user"]
            
        return data

    class Config:
        from_attributes = True

class CommunityPostListResponse(BaseModel):
    items: List[CommunityPost]
    meta: PaginationMeta
