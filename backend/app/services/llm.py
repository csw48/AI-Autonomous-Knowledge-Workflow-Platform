"""LLM service abstractions live here."""

from collections.abc import Mapping
from typing import Any


class LLMService:
    """Stub for future LLM provider integration."""

    def __init__(self, provider: str) -> None:
        self.provider = provider

    async def generate(self, prompt: str, **kwargs: Any) -> Mapping[str, Any]:
        raise NotImplementedError("LLM integration not implemented yet")
