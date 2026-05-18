from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

# Importamos el modelo de actividades que crearon tus compañeros
from app.models.activity import Activity 

router = APIRouter()

# Quitamos el candado (authenticate) y abrimos la conexión a la base de datos (get_db)
@router.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    # Buscamos todas las actividades en la tabla real de la base de datos
    activities = db.query(Activity).all()
    return activities