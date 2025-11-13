import importlib

import pytest_asyncio


@pytest_asyncio.fixture
async def db_session(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

    from backend.app.core import config as config_module

    config_module.get_settings.cache_clear()

    import backend.app.db.session as session_module

    session_module = importlib.reload(session_module)
    await session_module.init_db()

    try:
        sessionmaker = session_module.get_sessionmaker()
        async with sessionmaker() as session:
            yield session
    finally:
        await session_module.close_db()
