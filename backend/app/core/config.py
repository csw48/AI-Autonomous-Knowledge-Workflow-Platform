from functools import lru_cache
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

    notion_api_key: str | None = None
    notion_database_id: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""

    return Settings()
