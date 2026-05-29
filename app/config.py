"""Application configuration management."""

import os
from functools import lru_cache
from typing import Optional


class Settings:
    """Application settings loaded from environment."""

    APP_NAME: str = os.getenv("APP_NAME", "bmdr-app")
    APP_ENV: str = os.getenv("APP_ENV", "dev")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")

    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")

    CF_TUNNEL_TOKEN: Optional[str] = os.getenv("CF_TUNNEL_TOKEN")

    @property
    def is_dev(self) -> bool:
        return self.APP_ENV == "dev"

    @property
    def is_prod(self) -> bool:
        return self.APP_ENV == "prod"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
