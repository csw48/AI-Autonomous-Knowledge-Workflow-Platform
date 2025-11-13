from __future__ import annotations

import logging
from typing import Any

from backend.app.core.config import Settings, get_settings
from httpx import AsyncClient, Response

logger = logging.getLogger(__name__)


class NotionClient:
    """Thin wrapper around Notion API for milestone tracking."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.base_url = "https://api.notion.com/v1"
        self._headers = {
            "Authorization": (
                f"Bearer {self.settings.notion_api_key}" if self.settings.notion_api_key else ""
            ),
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        return bool(self.settings.notion_api_key and self.settings.notion_database_id)

    async def update_task_status(self, task_name: str, status: str) -> None:
        if not self.is_configured():
            logger.info("Notion credentials missing; skipping update for task '%s'", task_name)
            return

        async with AsyncClient(base_url=self.base_url, headers=self._headers) as client:
            payload: dict[str, Any] = {"task": task_name, "status": status}
            response: Response = await client.post("/placeholder", json=payload)
            logger.debug("Notion response: %s", response.status_code)
