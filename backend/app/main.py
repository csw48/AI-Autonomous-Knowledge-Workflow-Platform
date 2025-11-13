from fastapi import FastAPI

from backend.app.api.routes import health
from backend.app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.include_router(health.router, prefix="/api/v1")

    return app


app = create_app()
