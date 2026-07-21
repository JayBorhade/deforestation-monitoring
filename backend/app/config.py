"""Application configuration and settings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = "postgresql://deforestation:deforestation@db:5432/deforestation_db"
    database_echo: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    api_title: str = "Deforestation Monitoring API"
    api_version: str = "0.1.0"
    api_description: str = "AI-powered satellite monitoring for deforestation detection"

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Environment
    environment: str = "development"
    debug: bool = True

    # File Storage
    upload_dir: str = "/app/uploads"
    models_dir: str = "/app/models"

    # ML Models
    deforestation_model_path: str = "/app/models/deforestation_unet.pth"

    # Logging
    log_level: str = "INFO"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get application settings (cached)."""
    return Settings()
