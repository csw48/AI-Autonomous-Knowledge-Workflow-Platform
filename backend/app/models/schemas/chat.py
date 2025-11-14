from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt to send to the LLM")


class ChatResponse(BaseModel):
    provider: str
    answer: str


class RagChatRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language RAG query")
    top_k: int = Field(default=5, ge=1, le=20)


class RagContext(BaseModel):
    document_id: str
    chunk_index: int
    content: str


class RagChatResponse(BaseModel):
    provider: str
    answer: str
    contexts: list[RagContext]
