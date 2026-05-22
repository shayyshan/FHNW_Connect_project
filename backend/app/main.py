import uvicorn
from app.api.routers import health, users, clubs, activities, announcements, auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.init_db import init_db

# Creates the main FastAPI application
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        docs_url="/docs",  # Swagger UI endpoint
    )

    # Allows front-ends from different domains to communicate with this backend
    # Basic CORS setup
    if settings.cors_origins_list:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins_list,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Register routers
    app.include_router(health.router, prefix=settings.API_PREFIX, tags=["Health"])
    app.include_router(users.router, prefix=settings.API_PREFIX, tags=["Users"])
    app.include_router(clubs.router, prefix=settings.API_PREFIX, tags=["Clubs"])
    app.include_router(activities.router, prefix=settings.API_PREFIX, tags=["Activities"])
    app.include_router(announcements.router, prefix=settings.API_PREFIX, tags=["Announcements"])
    app.include_router(auth.router, prefix=settings.API_PREFIX, tags=["Auth"])

    # Root endpoint
    @app.get("/")
    def read_root():
        return {"message": "FHNW Connect API is running"}

    # This code runs automatically when the server starts up
    @app.on_event("startup")
    def on_startup():
        # Calls our function to set up the database and insert dummy data
        init_db()

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=True
    )
