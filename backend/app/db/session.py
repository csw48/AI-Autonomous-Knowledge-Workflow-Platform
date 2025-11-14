from __future__ import annotations

import asyncio
import logging
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.app.core.config import get_settings
from backend.app.db.base import Base

logger = logging.getLogger(__name__)

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(settings.database_url, echo=False, future=True)
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global _sessionmaker
    if _sessionmaker is None:
        _sessionmaker = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
    return _sessionmaker


async def get_db_session() -> AsyncIterator[AsyncSession]:
    sessionmaker = get_sessionmaker()
    async with sessionmaker() as session:
        yield session


async def init_db(retries: int = 8, base_delay: float = 1.0) -> None:
    attempt = 0
    while True:
        try:
            engine = get_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database ready")
            break
        except Exception as exc:  # pragma: no cover - exercised in container runtime
            attempt += 1
            if attempt >= retries:
                logger.exception("Database initialization failed after %s attempts", attempt)
                raise
            delay = base_delay * attempt
            logger.warning(
                "Database init attempt %s/%s failed: %s. Retrying in %.1fs",
                attempt,
                retries,
                exc,
                delay,
            )
            await asyncio.sleep(delay)


async def close_db() -> None:
    global _engine, _sessionmaker
    _sessionmaker = None
    if _engine:
        await _engine.dispose()
        _engine = None
