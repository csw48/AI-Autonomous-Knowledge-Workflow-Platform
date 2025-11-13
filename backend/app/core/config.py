from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "AI Autonomous Knowledge & Workflow Platform"
    debug: bool = False
    environment: str = "development"
    log_level: str = "INFO"

    openai_api_key: str | None = None
    llm_provider: str = "openai"

    database_url: str = "sqlite+aiosqlite:///./local.db"
    vector_db_url: str | None = None

    allowed_origins: list[str] = ["http://localhost:3000"]

    notion_api_key: str | None = None
    notion_database_id: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()
