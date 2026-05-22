from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.community_post import CommunityPost

router = APIRouter()

@router.get("/announcements")
def get_announcements(db: Session = Depends(get_db)):
    announcements = db.query(CommunityPost).filter(
        CommunityPost.community_post_category == "Announcements"
    ).all()
    return announcements