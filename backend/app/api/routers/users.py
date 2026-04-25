from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.security import authenticate
router = APIRouter()

# This creates a GET endpoint at /api/users. It returns a list of UserResponse objects
@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    # Fetches every user currently in the database table and returns them
    users = db.query(User).all()
    return users
@router.get("/user")
def user_content(current_user=Depends(authenticate)):
    if current_user["role"] != "USER":
        raise HTTPException(status_code=403, detail="Access denied")

    return {"message":"Only a user can view this content."}


@router.get("/admin")
def admin_content(current_user=Depends(authenticate)):
    if current_user["role"] != "ADMIN":
        raise HTTPException(status_code=403, detail="Access denied")

    return {"message":"Only an admin can view this content."}