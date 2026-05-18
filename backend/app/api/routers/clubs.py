from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

# Asegúrate de que tus compañeros hayan creado este modelo en la carpeta models
from app.models.club import Club 

router = APIRouter()

@router.get("/clubs")
def get_clubs(db: Session = Depends(get_db)):
    # Busca todos los clubes en la base de datos real
    clubs = db.query(Club).all()
    return clubs