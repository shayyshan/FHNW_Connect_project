from fastapi import APIRouter, Depends
from app.core.security import authenticate

router = APIRouter()

@router.get("/activities")
def get_activities(user = Depends(authenticate)):
    return [{"id": 1, "title": "Football Tournament"}]