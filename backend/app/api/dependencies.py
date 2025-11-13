from collections.abc import AsyncIterator

from backend.app.core.config import Settings, get_settings
from backend.app.db.session import get_db_session
from backend.app.services.llm import LLMService
from sqlalchemy.ext.asyncio import AsyncSession


def get_app_settings() -> Settings:
    """FastAPI dependency hook for Settings."""

    return get_settings()


def get_llm_service() -> LLMService:
    """Provide an LLM service using the current application settings."""

    settings = get_settings()
    return LLMService(settings)


async def get_db() -> AsyncIterator[AsyncSession]:
    """Yield an async database session for FastAPI dependencies."""

    async for session in get_db_session():
        yield session
