"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Environment = Literal["development", "testing", "staging", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Runtime settings for the ATHENA backend."""

    app_name: str = "ATHENA"
    app_version: str = "0.1.0"
    environment: Environment = "development"
    debug: bool = False
    log_level: LogLevel = "INFO"

    api_prefix: str = "/api/v1"
    request_id_header: str = "X-Request-ID"
    cors_allow_origins: list[str] = ["*"]
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    cors_allow_headers: list[str] = ["*"]
    database_url: str = Field(
        default="postgresql+asyncpg://athena:athena@localhost:5432/athena",
        repr=False,
    )
    redis_url: str = Field(default="redis://localhost:6379/0", repr=False)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="ATHENA_",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""

    return Settings()
