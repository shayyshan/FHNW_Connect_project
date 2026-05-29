from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "FHNW Connect API"
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    PORT: int = 10000

    # Database
    DATABASE_URL: str = "postgresql://fhnw_connect_user:882xQ8h7V3Xf7i9NoiwRScj0OAN74mNP@dpg-d886cagg4nts73eqsu30-a.frankfurt-postgres.render.com/fhnw_connect"

    # CORS
    CORS_ORIGINS: str = ""

    # Basic auth credentials for Render/deployment
    BASIC_AUTH_USER: str = "myuser"
    BASIC_AUTH_PASSWORD: str = "password"
    BASIC_AUTH_ADMIN: str = "myadmin"
    BASIC_AUTH_ADMIN_PASSWORD: str = "password"

    @property
    def cors_origins_list(self) -> List[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
