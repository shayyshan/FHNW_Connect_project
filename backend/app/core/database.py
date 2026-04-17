from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Hardcoded SQLite configuration
DATABASE_URL = "sqlite:///./fhnw_connect.db"

# This is the main connection engine that talks to our SQLite database file
# Create SQLite engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# This creates a factory that gives us individual database sessions (like a separate conversation with the DB)
# Session factory
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
