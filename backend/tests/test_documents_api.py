import pytest
from backend.app.api.dependencies import get_db
from backend.app.core import config as config_module
from backend.app.main import create_app
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_upload_document_endpoint(db_session, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    config_module.get_settings.cache_clear()

    test_app = create_app()

    async def _override_db():
        yield db_session

    test_app.dependency_overrides[get_db] = _override_db

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        files = {"file": ("notes.txt", b"hello world\nthis is a test", "text/plain")}
        response = await client.post("/api/v1/documents", files=files)

    test_app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert payload["chunk_count"] >= 1
    assert payload["title"] == "notes.txt"
