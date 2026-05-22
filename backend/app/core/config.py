from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FHNW Connect API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    PORT: int = 10000

    # Database
    DATABASE_URL: str = "postgresql+psycopg://postgres:postgres@localhost:5432/fhnw_connect"
    RECREATE_DB: bool = False

    # CORS
    CORS_ORIGINS: str = ""

    # Basic auth credentials for Render/deployment
    BASIC_AUTH_USER: str = "myuser"
    BASIC_AUTH_PASSWORD: str = "password"
    BASIC_AUTH_ADMIN: str = "myadmin"
    BASIC_AUTH_ADMIN_PASSWORD: str = "password"

    # JWT Security Configuration
    SECRET_KEY: str = "replace-with-a-secure-random-key-for-jwt-signing"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours, convenient for Budibase Cloud

    @property
    def cors_origins_list(self) -> List[str]:
        if not self.CORS_ORIGINS:
            return []
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

