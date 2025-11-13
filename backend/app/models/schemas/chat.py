from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt to send to the LLM")


class ChatResponse(BaseModel):
    provider: str
    answer: str
