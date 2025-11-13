from backend.app.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    """FastAPI dependency hook for Settings."""

    return get_settings()
