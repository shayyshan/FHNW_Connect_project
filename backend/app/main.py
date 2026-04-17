from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routers import health, users

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

    # Adds our specific route endpoints to the main application
    # Register routers
    app.include_router(health.router, prefix=settings.API_PREFIX, tags=["Health"])
    app.include_router(users.router, prefix=settings.API_PREFIX, tags=["Users"])

    from app.core.init_db import init_db
    
    # This code runs automatically when the server starts up
    @app.on_event("startup")
    def on_startup():
        # Calls our function to set up the database and insert dummy data
        init_db()

    return app

app = create_app()
