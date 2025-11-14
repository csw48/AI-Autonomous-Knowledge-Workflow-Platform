from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import get_db, get_llm_service
from backend.app.models.schemas.agents import (
    AgentExecuteRequest,
    AgentExecuteResponse,
    AgentStepModel,
)
from backend.app.services.agents import DocumentSearchTool, SimpleAgent
from backend.app.services.llm import LLMService

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/execute", response_model=AgentExecuteResponse)
async def execute_agent(
    payload: AgentExecuteRequest,
    db: AsyncSession = Depends(get_db),
    llm_service: LLMService = Depends(get_llm_service),
) -> AgentExecuteResponse:
    """Execute a simple multi-step agent over stored documents."""

    tool = DocumentSearchTool(db)
    agent = SimpleAgent(llm=llm_service, tools=[tool])
    result = await agent.execute(goal=payload.goal, max_chunks=payload.max_chunks)

    return AgentExecuteResponse(
        answer=result.answer,
        steps=[
            AgentStepModel(
                kind=step.kind,
                message=step.message,
                tool_name=step.tool_name,
                tool_input=step.tool_input,
                tool_output=step.tool_output,
            )
            for step in result.steps
        ],
    )

