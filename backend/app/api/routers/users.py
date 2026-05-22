from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import datetime

from app.core.database import get_db
from app.models.user import User
from app.models.activity import Activity
from app.models.user_activity import UserActivity
from app.schemas.user import User as UserSchema
from app.schemas.dashboard import DashboardResponse
from app.core.security import get_current_user

# We reuse helpers to build the dashboard
from app.schemas.activity import ActivitySummary
from app.schemas.club import ClubSummary

router = APIRouter()

def make_activity_summary(activity, current_user, db):
    joined_count = db.query(UserActivity).filter(
        UserActivity.activity_id == activity.activity_id,
        UserActivity.registration_status == "joined"
    ).count()
    
    available_slots = (activity.max_slots - joined_count) if activity.max_slots is not None else 0
    if available_slots < 0:
        available_slots = 0
        
    is_favorited = activity in current_user.favorite_activities if current_user else False
    
    my_reg = None
    if current_user:
        user_act = db.query(UserActivity).filter(
            UserActivity.activity_id == activity.activity_id,
            UserActivity.user_id == current_user.user_id
        ).first()
        if user_act:
            my_reg = user_act.registration_status
            
    club_sum = None
    if activity.club:
        is_club_fav = activity.club in current_user.favorite_clubs if current_user else False
        club_sum = ClubSummary(
            club_id=activity.club.club_id,
            club_name=activity.club.club_name,
            club_description=activity.club.club_description,
            image_path=activity.club.image_path,
            is_favorited=is_club_fav
        )

    return ActivitySummary(
        activity_id=activity.activity_id,
        activity_title=activity.activity_title,
        activity_description=activity.activity_description,
        activity_location=activity.activity_location,
        max_slots=activity.max_slots,
        activity_category=activity.activity_category,
        image_path=activity.image_path,
        club_id=activity.club_id,
        club=club_sum,
        joined_count=joined_count,
        available_slots=available_slots,
        is_favorited=is_favorited,
        my_registration_status=my_reg
    )

def make_club_summary(club, current_user):
    is_favorited = club in current_user.favorite_clubs if current_user else False
    return ClubSummary(
        club_id=club.club_id,
        club_name=club.club_name,
        club_description=club.club_description,
        image_path=club.image_path,
        is_favorited=is_favorited
    )


@router.get("/users", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/users/me", response_model=UserSchema)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/me/dashboard", response_model=DashboardResponse)
def get_dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # 1. Calendar Items (Activities joined by the current user)
    joined_activities = db.query(Activity).join(UserActivity).filter(
        UserActivity.user_id == current_user.user_id,
        UserActivity.registration_status == "joined"
    ).all()
    calendar_items = [make_activity_summary(act, current_user, db) for act in joined_activities]

    # 2. Upcoming Activities (Events in the future, e.g. next 30 days)
    today = datetime.datetime.now()
    upcoming_db = db.query(Activity).filter(
        Activity.start_date >= today
    ).order_by(Activity.start_date.asc()).limit(10).all()
    upcoming_activities = [make_activity_summary(act, current_user, db) for act in upcoming_db]

    # 3. Favorite Clubs
    favorite_clubs = [make_club_summary(club, current_user) for club in current_user.favorite_clubs]

    # 4. Favorite Activities
    favorite_activities = [make_activity_summary(act, current_user, db) for act in current_user.favorite_activities]

    return DashboardResponse(
        calendar_items=calendar_items,
        upcoming_activities=upcoming_activities,
        favorite_clubs=favorite_clubs,
        favorite_activities=favorite_activities
    )