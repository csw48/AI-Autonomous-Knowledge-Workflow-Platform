"""LLM service abstractions live here."""

from __future__ import annotations

from dataclasses import dataclass

from backend.app.core.config import Settings


@dataclass
class LLMResponse:
    provider: str
    answer: str


class LLMService:
    """Lightweight LLM facade with deterministic fallback behaviour."""

    def __init__(self, settings: Settings) -> None:
        self.provider = settings.llm_provider
        self.api_key = settings.openai_api_key

    async def chat(self, prompt: str) -> LLMResponse:
        """Return a deterministic answer until a real provider integration is added."""

        normalized_prompt = prompt.strip()
        if not normalized_prompt:
            raise ValueError("Prompt must not be empty.")

        if not self.api_key:
            fallback = f"[stub:{self.provider}] {normalized_prompt}"
            return LLMResponse(provider=self.provider, answer=fallback)

        # Placeholder for real provider integration (OpenAI, Claude, etc.)
        fallback = f"[provider:{self.provider}] {normalized_prompt}"
        return LLMResponse(provider=self.provider, answer=fallback)
