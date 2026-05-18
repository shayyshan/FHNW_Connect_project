from fastapi import APIRouter, Depends
from app.core.security import authenticate

router = APIRouter()

@router.get("/clubs")
def get_clubs(user = Depends(authenticate)):
    return [{"id": 1, "name": "Tech Club"}]