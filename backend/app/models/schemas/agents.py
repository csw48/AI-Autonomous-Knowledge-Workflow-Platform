from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class AgentExecuteRequest(BaseModel):
    goal: str = Field(..., min_length=1, description="High-level goal for the agent to solve")
    max_chunks: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of document chunks to retrieve via tools",
    )


class AgentStepModel(BaseModel):
    kind: str
    message: str
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None
    tool_output: dict[str, Any] | None = None


class AgentExecuteResponse(BaseModel):
    answer: str
    steps: list[AgentStepModel]

