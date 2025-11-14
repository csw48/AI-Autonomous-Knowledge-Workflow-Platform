import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.main import app


@pytest.mark.asyncio
async def test_chat_endpoint_returns_stubbed_answer() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.post("/api/v1/chat", json={"prompt": "Hello"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["provider"] == "openai"
    assert payload["answer"].startswith("[stub:openai]")
