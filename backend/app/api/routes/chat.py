from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_db, get_llm_service
from backend.app.models.schemas.chat import (
    ChatRequest,
    ChatResponse,
    RagChatRequest,
    RagChatResponse,
    RagContext,
)
from backend.app.services.llm import LLMService
from backend.app.services.search import SearchService

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    body: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service),
) -> ChatResponse:
    """Return a simple LLM-generated response for the provided prompt."""

    result = await llm_service.chat(body.prompt)
    return ChatResponse(provider=result.provider, answer=result.answer)


@router.post("/chat/rag", response_model=RagChatResponse)
async def chat_rag_endpoint(
    body: RagChatRequest,
    db: AsyncSession = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service),
) -> RagChatResponse:
    """RAG-style chat that retrieves document chunks before answering."""

    search_service = SearchService(db)
    # Prefer vector search (pgvector) with a graceful fallback to keyword search.
    matches = await search_service.search_by_vector(query=body.query, limit=body.top_k)

    if not matches:
        answer = "No relevant documents found for your query yet. Try uploading more context."
        return RagChatResponse(provider=llm_service.provider, answer=answer, contexts=[])

    context_lines = [f"[{m['document_id']}#{m['chunk_index']}] {m['content']}" for m in matches]
    prompt = (
        "You are a retrieval-augmented assistant. Use ONLY the provided "
        "context to answer the user's question.\n\n"
        f"Question: {body.query}\n\nContext:\n" + "\n".join(context_lines)
    )

    llm_result = await llm_service.chat(prompt)
    return RagChatResponse(
        provider=llm_result.provider,
        answer=llm_result.answer,
        contexts=[
            RagContext(
                document_id=m["document_id"],
                chunk_index=m["chunk_index"],
                content=m["content"],
            )
            for m in matches
        ],
    )
