from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Read the database URL from environment variables
DATABASE_URL = settings.DATABASE_URL

# Ensure SQLAlchemy uses the psycopg3 driver when a generic PostgreSQL URL is provided
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

if connect_args:
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        future=True,
    )
else:
    engine = create_engine(
        DATABASE_URL,
        future=True,
    )

# This creates a factory that gives us individual database sessions (like a separate conversation with the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A helper function to give each web request its own database session
def get_db():
    """
    Dependency to provide a database session for a single request.
    Closes the session after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
