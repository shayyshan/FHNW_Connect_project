from fastapi import APIRouter, Depends
from app.core.security import authenticate

router = APIRouter()

@router.get("/announcements")
def get_announcements(user = Depends(authenticate)):
    return [{"id": 1, "title": "Welcome Event"}]