from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import datetime

from app.core.database import get_db
from app.models.club import Club
from app.models.activity import Activity
from app.models.community_post import CommunityPost
from app.models.user import User
from app.schemas.club import (
    ClubSummary, ClubDetail, ClubCreate, ClubUpdate, ClubListResponse
)
from app.schemas.activity import ActivityListResponse
from app.schemas.community_post import CommunityPostListResponse
from app.schemas.common import PaginationMeta
from app.core.security import get_current_user
from app.api.routers.activities import get_current_user_optional, make_activity_summary

router = APIRouter()

def make_club_summary(club: Club, current_user: Optional[User]) -> ClubSummary:
    is_favorited = club in current_user.favorite_clubs if current_user else False
    return ClubSummary(
        club_id=club.club_id,
        club_name=club.club_name,
        club_description=club.club_description,
        image_path=club.image_path,
        is_favorited=is_favorited
    )

def make_club_detail(club: Club, current_user: Optional[User], db: Session) -> ClubDetail:
    is_favorited = club in current_user.favorite_clubs if current_user else False
    now = datetime.datetime.now()
    upcoming_count = db.query(Activity).filter(
        Activity.club_id == club.club_id,
        Activity.start_date >= now
    ).count()
    return ClubDetail(
        club_id=club.club_id,
        club_name=club.club_name,
        club_description=club.club_description,
        image_path=club.image_path,
        is_favorited=is_favorited,
        upcoming_activities_count=upcoming_count
    )


@router.get("/clubs", response_model=ClubListResponse)
def get_clubs(
    search: Optional[str] = None,
    only_favorites: Optional[bool] = False,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Club)

    if search:
        query = query.filter(
            or_(
                Club.club_name.ilike(f"%{search}%"),
                Club.club_description.ilike(f"%{search}%")
            )
        )

    if only_favorites and current_user:
        fav_ids = [c.club_id for c in current_user.favorite_clubs]
        query = query.filter(Club.club_id.in_(fav_ids))

    total_items = query.count()
    offset = (page - 1) * page_size
    clubs = query.offset(offset).limit(page_size).all()
    
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    items = [make_club_summary(c, current_user) for c in clubs]
    
    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages
    )

    return ClubListResponse(items=items, meta=meta)


@router.post("/clubs", response_model=ClubDetail, status_code=status.HTTP_201_CREATED)
def create_club(
    payload: ClubCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check duplicate name
    existing = db.query(Club).filter(Club.club_name == payload.club_name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Club with this name already exists"
        )

    new_club = Club(
        club_name=payload.club_name,
        club_description=payload.club_description,
        image_path=payload.image_path
    )
    db.add(new_club)
    db.commit()
    db.refresh(new_club)

    return make_club_detail(new_club, current_user, db)


@router.get("/clubs/{clubId}", response_model=ClubDetail)
def get_club_by_id(
    clubId: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    return make_club_detail(club, current_user, db)


@router.patch("/clubs/{clubId}", response_model=ClubDetail)
def update_club(
    clubId: int,
    payload: ClubUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )

    update_data = payload.dict(exclude_unset=True)
    if "club_name" in update_data and update_data["club_name"] != club.club_name:
        existing = db.query(Club).filter(Club.club_name == update_data["club_name"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Club with this name already exists"
            )

    for field, value in update_data.items():
        setattr(club, field, value)

    db.commit()
    db.refresh(club)
    return make_club_detail(club, current_user, db)


@router.delete("/clubs/{clubId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_club(
    clubId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )
    db.delete(club)
    db.commit()
    return None


@router.get("/clubs/{clubId}/activities", response_model=ActivityListResponse)
def get_club_activities(
    clubId: int,
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )

    query = db.query(Activity).filter(Activity.club_id == clubId)

    if date_from:
        query = query.filter(Activity.start_date >= datetime.datetime.combine(date_from, datetime.time.min))
    if date_to:
        query = query.filter(Activity.start_date <= datetime.datetime.combine(date_to, datetime.time.max))

    total_items = query.count()
    offset = (page - 1) * page_size
    activities = query.offset(offset).limit(page_size).all()
    
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    items = [make_activity_summary(act, current_user, db) for act in activities]

    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages
    )

    return ActivityListResponse(items=items, meta=meta)


@router.get("/clubs/{clubId}/announcements", response_model=CommunityPostListResponse)
def get_club_announcements(
    clubId: int,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )

    query = db.query(CommunityPost).filter(
        CommunityPost.club_id == clubId,
        CommunityPost.community_post_category == "announcement"
    )

    total_items = query.count()
    offset = (page - 1) * page_size
    posts = query.offset(offset).limit(page_size).all()
    
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages
    )

    return CommunityPostListResponse(items=posts, meta=meta)


@router.put("/clubs/{clubId}/favorite", status_code=status.HTTP_204_NO_CONTENT)
def favorite_club(
    clubId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )

    if club not in current_user.favorite_clubs:
        current_user.favorite_clubs.append(club)
        db.commit()
    return None


@router.delete("/clubs/{clubId}/favorite", status_code=status.HTTP_204_NO_CONTENT)
def unfavorite_club(
    clubId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    club = db.query(Club).filter(Club.club_id == clubId).first()
    if not club:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Club not found"
        )

    if club in current_user.favorite_clubs:
        current_user.favorite_clubs.remove(club)
        db.commit()
    return None