import pytest
from backend.app.api.dependencies import get_db
from backend.app.core import config as config_module
from backend.app.main import create_app
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_search_endpoint_returns_matches(db_session, monkeypatch):
    # Force SQLite in-memory for test isolation
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    config_module.get_settings.cache_clear()

    app = create_app()

    async def _override_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Seed a small document via the public endpoint
        files = {"file": ("seed.txt", b"hello world\nsearch me please", "text/plain")}
        upload = await client.post("/api/v1/documents", files=files)
        assert upload.status_code == 200

        # Search for a known token
        response = await client.post("/api/v1/search", json={"query": "hello", "limit": 5})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert any("hello" in item["content"].lower() for item in data)

        # Longer natural-language query should still hit via token matching
        response2 = await client.post(
            "/api/v1/search",
            json={"query": "What does the hello world document contain?", "limit": 5},
        )
        assert response2.status_code == 200
        data2 = response2.json()
        assert isinstance(data2, list)
        assert any("hello" in item["content"].lower() for item in data2)

    app.dependency_overrides.clear()
