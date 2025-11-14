import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.api.dependencies import get_db
from backend.app.core import config as config_module
from backend.app.main import create_app


@pytest.mark.asyncio
async def test_agent_execute_uses_document_search_and_returns_steps(db_session, monkeypatch):
    # Use in-memory SQLite for isolation
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
    config_module.get_settings.cache_clear()

    app = create_app()

    async def _override_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Seed one document so the agent's search tool has something to find
        files = {"file": ("agent-notes.txt", b"hello world from the agent test", "text/plain")}
        upload = await client.post("/api/v1/documents", files=files)
        assert upload.status_code == 200

        response = await client.post(
            "/api/v1/agents/execute",
            json={"goal": "Find info about hello world", "max_chunks": 3},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload["answer"], str)
    assert payload["answer"]
    assert isinstance(payload["steps"], list)
    kinds = [step["kind"] for step in payload["steps"]]
    assert "plan" in kinds
    assert "tool_call" in kinds
    assert "answer" in kinds

