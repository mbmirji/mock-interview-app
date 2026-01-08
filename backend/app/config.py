from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Literal


class Settings(BaseSettings):
    # Application settings
    app_name: str = "Mock Interview API"
    debug: bool = True
    environment: Literal["development", "staging", "production"] = "development"

    # Database settings (Supabase PostgreSQL)
    # Format: postgresql://postgres:[password]@[host]:[port]/postgres
    database_url: str = "postgresql://user:password@localhost:5432/mock_interview_db"

    # LLM settings (Google Gemini)
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"  # Options: gemini-1.5-flash, gemini-1.5-pro

    # File upload settings
    max_file_size_mb: int = 10
    allowed_extensions: list = [".pdf", ".doc", ".docx"]

    # Railway deployment settings
    port: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()
