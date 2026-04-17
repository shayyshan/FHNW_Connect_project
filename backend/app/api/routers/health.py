from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.schemas.health import HealthResponse

router = APIRouter()

# This creates a GET endpoint at /api/health. It returns a HealthResponse object to verify the API works.
@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """
    Verify API and Database health.
    """
    # --- DB check enabled ---
    try:
        db.execute(text("SELECT 1"))
        return HealthResponse(status="ok", message="API and Database are operational.")
    except Exception as e:
        return HealthResponse(status="error", message="Database connection failed.")
    
    # --- DB check disabled (Fallback) ---
    # To disable the DB check, comment out the try/except block above
    # and uncomment the line below:
    # return HealthResponse(status="ok", message="API is running")
