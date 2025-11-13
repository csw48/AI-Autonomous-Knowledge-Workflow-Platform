from backend.app.api.dependencies import get_llm_service
from backend.app.models.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.llm import LLMService
from fastapi import APIRouter, Depends

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    body: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service),
) -> ChatResponse:
    """Return a simple LLM-generated response for the provided prompt."""

    result = await llm_service.chat(body.prompt)
    return ChatResponse(provider=result.provider, answer=result.answer)
