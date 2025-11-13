from backend.app.core.config import Settings, get_settings
from backend.app.services.llm import LLMService


def get_app_settings() -> Settings:
    """FastAPI dependency hook for Settings."""

    return get_settings()


def get_llm_service() -> LLMService:
    """Provide an LLM service using the current application settings."""

    settings = get_settings()
    return LLMService(settings)
