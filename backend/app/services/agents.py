from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from backend.app.services.llm import LLMService
from backend.app.services.search import SearchService
from sqlalchemy.ext.asyncio import AsyncSession


class Tool(Protocol):
    name: str
    description: str

    async def run(self, *, input: dict[str, Any]) -> dict[str, Any]:
        ...


class DocumentSearchTool:
    """Tool that performs semantic/keyword search over stored document chunks."""

    name = "document_search"
    description = (
        "Searches stored document chunks for helpful context. "
        "Input: {'query': str, 'limit': int}. "
        "Returns: {'matches': [{document_id, chunk_index, content}]}."
    )

    def __init__(self, session: AsyncSession) -> None:
        self._search = SearchService(session)

    async def run(self, *, input: dict[str, Any]) -> dict[str, Any]:
        query = str(input.get("query", "")).strip()
        if not query:
            return {"matches": []}

        limit_raw = input.get("limit", 5)
        try:
            limit = int(limit_raw)
        except (TypeError, ValueError):
            limit = 5

        matches = await self._search.search_by_vector(query=query, limit=limit)
        return {"matches": matches}


@dataclass
class AgentStep:
    """Single reasoning step or tool invocation in the agent trace."""

    kind: str
    message: str
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None
    tool_output: dict[str, Any] | None = None


@dataclass
class AgentResult:
    answer: str
    steps: list[AgentStep]


class SimpleAgent:
    """A minimal planner/executor agent for multi-step document Q&A.

    Strategy:
    - Always run `document_search` first to gather context.
    - Then call the LLM with a prompt that includes the goal and retrieved chunks.
    - Return the final answer plus a lightweight trace of steps.
    """

    def __init__(self, llm: LLMService, tools: list[Tool]) -> None:
        self._llm = llm
        self._tools: dict[str, Tool] = {tool.name: tool for tool in tools}

    async def execute(self, goal: str, *, max_chunks: int = 5) -> AgentResult:
        steps: list[AgentStep] = []
        normalized_goal = goal.strip()

        if not normalized_goal:
            raise ValueError("Goal must not be empty.")

        # Step 1: plan
        steps.append(
            AgentStep(
                kind="plan",
                message="Analyze goal and decide which tool to call.",
            )
        )

        # Step 2: search via tool
        search_tool = self._tools.get("document_search")
        matches: list[dict[str, Any]] = []
        if search_tool is not None:
            tool_input = {"query": normalized_goal, "limit": max_chunks}
            tool_output = await search_tool.run(input=tool_input)
            matches = list(tool_output.get("matches", []))
            steps.append(
                AgentStep(
                    kind="tool_call",
                    message="Ran document_search to retrieve relevant chunks.",
                    tool_name=search_tool.name,
                    tool_input=tool_input,
                    tool_output={"match_count": len(matches)},
                )
            )

        # Step 3: answer with LLM
        context_lines: list[str] = []
        for match in matches[:max_chunks]:
            context_lines.append(
                f"[{match.get('document_id')}#{match.get('chunk_index')}] {match.get('content')}"
            )

        if context_lines:
            prompt = (
                "You are an AI agent with access to document search results.\n"
                "Use ONLY the provided context chunks to answer the user's goal.\n\n"
                f"Goal: {normalized_goal}\n\n"
                "Context:\n"
                + "\n".join(context_lines)
            )
        else:
            prompt = (
                "You are an AI agent, but document search returned no context.\n"
                "Explain that no documents match yet and suggest what the user could upload.\n\n"
                f"Goal: {normalized_goal}"
            )

        llm_response = await self._llm.chat(prompt)
        steps.append(
            AgentStep(
                kind="answer",
                message="Produced a final answer using the LLM.",
            )
        )

        return AgentResult(answer=llm_response.answer, steps=steps)

