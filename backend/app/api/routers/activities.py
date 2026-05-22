from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import datetime
import jwt

from app.core.database import get_db
from app.models.activity import Activity 
from app.models.user import User
from app.models.user_activity import UserActivity
from app.schemas.activity import (
    ActivitySummary, ActivityDetail, ActivityCreate, ActivityUpdate,
    ActivityListResponse, Registration, RegistrationStatus, RegistrationListResponse
)
from app.schemas.club import ClubSummary
from app.core.security import get_current_user
from app.core.config import settings

router = APIRouter()

def get_current_user_optional(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email:
            return db.query(User).filter(User.email == email).first()
    except:
        pass
    return None

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


@router.get("/activities", response_model=ActivityListResponse)
def get_activities(
    search: Optional[str] = None,
    category: Optional[str] = None,
    club_id: Optional[int] = None,
    location: Optional[str] = None,
    date_from: Optional[datetime.date] = None,
    date_to: Optional[datetime.date] = None,
    only_favorites: Optional[bool] = False,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    query = db.query(Activity)

    # Filtering
    if search:
        query = query.filter(
            or_(
                Activity.activity_title.ilike(f"%{search}%"),
                Activity.activity_description.ilike(f"%{search}%")
            )
        )
    if category:
        query = query.filter(Activity.activity_category == category)
    if club_id:
        query = query.filter(Activity.club_id == club_id)
    if location:
        query = query.filter(Activity.activity_location.ilike(f"%{location}%"))
    if date_from:
        query = query.filter(Activity.start_date >= datetime.datetime.combine(date_from, datetime.time.min))
    if date_to:
        query = query.filter(Activity.start_date <= datetime.datetime.combine(date_to, datetime.time.max))
    if only_favorites and current_user:
        fav_ids = [act.activity_id for act in current_user.favorite_activities]
        query = query.filter(Activity.activity_id.in_(fav_ids))

    # Pagination
    total_items = query.count()
    offset = (page - 1) * page_size
    activities = query.offset(offset).limit(page_size).all()
    
    total_pages = (total_items + page_size - 1) // page_size if total_items > 0 else 1

    items = [make_activity_summary(act, current_user, db) for act in activities]

    from app.schemas.common import PaginationMeta
    meta = PaginationMeta(
        page=page,
        page_size=page_size,
        total_items=total_items,
        total_pages=total_pages
    )

    return ActivityListResponse(items=items, meta=meta)


@router.post("/activities", response_model=ActivityDetail, status_code=status.HTTP_201_CREATED)
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    start_dt = datetime.datetime.now()
    end_dt = datetime.datetime.now() + datetime.timedelta(hours=2)
    if payload.activity_date:
        s_time = payload.start_time or datetime.time(12, 0)
        e_time = payload.end_time or datetime.time(14, 0)
        start_dt = datetime.datetime.combine(payload.activity_date, s_time)
        end_dt = datetime.datetime.combine(payload.activity_date, e_time)

    new_activity = Activity(
        activity_title=payload.activity_title,
        activity_description=payload.activity_description,
        start_date=start_dt,
        end_date=end_dt,
        activity_location=payload.activity_location,
        max_slots=payload.max_slots,
        activity_category=payload.activity_category,
        image_path=payload.image_path,
        club_id=payload.club_id
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return make_activity_summary(new_activity, current_user, db)


@router.get("/activities/{activityId}", response_model=ActivityDetail)
def get_activity_details(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    activity = db.query(Activity).filter(Activity.activity_id == activityId).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return make_activity_summary(activity, current_user, db)


@router.patch("/activities/{activityId}", response_model=ActivityDetail)
def update_activity(
    activityId: int,
    payload: ActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = db.query(Activity).filter(Activity.activity_id == activityId).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    update_data = payload.dict(exclude_unset=True)

    if "activity_date" in update_data or "start_time" in update_data or "end_time" in update_data:
        curr_date = activity.start_date.date()
        curr_start = activity.start_date.time()
        curr_end = activity.end_date.time()

        if "activity_date" in update_data:
            curr_date = update_data["activity_date"]
        if "start_time" in update_data:
            curr_start = update_data["start_time"]
        if "end_time" in update_data:
            curr_end = update_data["end_time"]

        activity.start_date = datetime.datetime.combine(curr_date, curr_start)
        activity.end_date = datetime.datetime.combine(curr_date, curr_end)

    for field, value in update_data.items():
        if field not in ["activity_date", "start_time", "end_time"]:
            setattr(activity, field, value)

    db.commit()
    db.refresh(activity)
    return make_activity_summary(activity, current_user, db)


@router.delete("/activities/{activityId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = db.query(Activity).filter(Activity.activity_id == activityId).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    return None


# --- Registrations (Join / Leave) ---

@router.post("/activities/{activityId}/join", response_model=Registration)
def join_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = db.query(Activity).filter(Activity.activity_id == activityId).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    joined_count = db.query(UserActivity).filter(
        UserActivity.activity_id == activityId,
        UserActivity.registration_status == "joined"
    ).count()

    if activity.max_slots is not None and joined_count >= activity.max_slots:
        raise HTTPException(status_code=409, detail="No free slots available for this activity")

    registration = db.query(UserActivity).filter(
        UserActivity.activity_id == activityId,
        UserActivity.user_id == current_user.user_id
    ).first()

    if registration:
        if registration.registration_status == "joined":
            raise HTTPException(status_code=409, detail="User already registered for this activity")
        else:
            registration.registration_status = "joined"
            registration.joined_at = datetime.datetime.now()
    else:
        registration = UserActivity(
            user_id=current_user.user_id,
            activity_id=activityId,
            registration_status="joined"
        )
        db.add(registration)

    db.commit()
    db.refresh(registration)
    return registration


@router.post("/activities/{activityId}/leave", response_model=Registration)
def leave_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    registration = db.query(UserActivity).filter(
        UserActivity.activity_id == activityId,
        UserActivity.user_id == current_user.user_id
    ).first()

    if not registration:
        raise HTTPException(status_code=404, detail="No registration found for this activity")

    registration.registration_status = "left"
    db.commit()
    db.refresh(registration)
    return registration


@router.get("/activities/{activityId}/registrations", response_model=RegistrationListResponse)
def get_registrations(
    activityId: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(UserActivity).filter(UserActivity.activity_id == activityId)
    if status:
        query = query.filter(UserActivity.registration_status == status)
    
    registrations = query.all()
    return RegistrationListResponse(items=registrations)


# --- Favorites ---

@router.put("/activities/{activityId}/favorite", status_code=status.HTTP_204_NO_CONTENT)
def favorite_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = db.query(Activity).filter(Activity.activity_id == activityId).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity not in current_user.favorite_activities:
        current_user.favorite_activities.append(activity)
        db.commit()
    return None


@router.delete("/activities/{activityId}/favorite", status_code=status.HTTP_204_NO_CONTENT)
def unfavorite_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    activity = db.query(Activity).filter(Activity.activity_id == activityId).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    if activity in current_user.favorite_activities:
        current_user.favorite_activities.remove(activity)
        db.commit()
    return None