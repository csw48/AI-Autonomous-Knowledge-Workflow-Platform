from contextlib import asynccontextmanager

from backend.app.api.routes import chat, health
from backend.app.core.config import get_settings
from backend.app.db.session import close_db, init_db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield
    await close_db()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.include_router(health.router, prefix="/api/v1")
    app.include_router(chat.router, prefix="/api/v1")

    return app


app = create_app()
