from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.models.club import Club 

router = APIRouter()

@router.get("/clubs")
def get_clubs(db: Session = Depends(get_db)):
    clubs = db.query(Club).all()
    return clubs