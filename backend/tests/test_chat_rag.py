import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.api.dependencies import get_db
from backend.app.core import config as config_module
from backend.app.main import create_app


@pytest.mark.asyncio
async def test_chat_rag_returns_contexts(db_session, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    config_module.get_settings.cache_clear()

    app = create_app()

    async def _override_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        files = {"file": ("rag.txt", b"rag test content", "text/plain")}
        upload = await client.post("/api/v1/documents", files=files)
        assert upload.status_code == 200

        response = await client.post("/api/v1/chat/rag", json={"query": "rag", "top_k": 5})
        assert response.status_code == 200
        data = response.json()
        assert data["provider"]
        assert isinstance(data["contexts"], list)
        assert any("rag" in ctx["content"].lower() for ctx in data["contexts"])

    app.dependency_overrides.clear()

