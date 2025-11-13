from backend.app.api.dependencies import get_app_settings
from backend.app.core.config import Settings
from backend.app.models.schemas.health import HealthResponse
from fastapi import APIRouter, Depends

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health(settings: Settings = Depends(get_app_settings)) -> HealthResponse:
    """Readiness probe for the API server."""

    detail = f"env={settings.environment}"
    return HealthResponse(status="ok", detail=detail)
