from __future__ import annotations

import logging
from typing import Any, Final

from httpx import AsyncClient, HTTPStatusError

from backend.app.core.config import Settings, get_settings

logger = logging.getLogger(__name__)

_STATUS_ALIASES: Final[dict[str, str]] = {
    "todo": "To Do",
    "to do": "To Do",
    "backlog": "To Do",
    "in progress": "In Progress",
    "progress": "In Progress",
    "working": "In Progress",
    "blocked": "Blocked",
    "done": "Done",
    "complete": "Done",
    "completed": "Done",
}


class NotionClient:
    """Thin wrapper around Notion API for milestone tracking."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.base_url = "https://api.notion.com/v1"
        self.database_id = self.settings.notion_database_id
        self._headers = {
            "Authorization": (
                f"Bearer {self.settings.notion_api_key}" if self.settings.notion_api_key else ""
            ),
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def is_configured(self) -> bool:
        return bool(self.settings.notion_api_key and self.database_id)

    async def update_task_status(self, task_name: str, status: str) -> None:
        """Set the Status column for the given Notion page."""

        if not self.is_configured():
            logger.info("Notion credentials missing; skipping update for task '%s'", task_name)
            return

        normalized = _STATUS_ALIASES.get(status.lower(), status)
        page = await self._find_task_page(task_name)
        if not page:
            logger.warning("Notion task '%s' not found; cannot update status", task_name)
            return

        page_id = page["id"]
        payload: dict[str, Any] = {"properties": {"Status": {"status": {"name": normalized}}}}

        async with AsyncClient(base_url=self.base_url, headers=self._headers) as client:
            response = await client.patch(f"/pages/{page_id}", json=payload)
            try:
                response.raise_for_status()
            except HTTPStatusError as exc:
                logger.error("Failed to update Notion task '%s': %s", task_name, exc)
                raise

        logger.info("Updated Notion task '%s' to status '%s'", task_name, normalized)

    async def log_milestone(self, task_name: str, details: dict[str, Any] | None = None) -> None:
        """Add a lightweight comment with milestone details to the task page."""

        if not details:
            logger.debug("No details supplied for task '%s'; skipping log entry", task_name)
            return

        if not self.is_configured():
            logger.info("Notion credentials missing; skipping log for task '%s'", task_name)
            return

        page = await self._find_task_page(task_name)
        if not page:
            logger.warning("Notion task '%s' not found; cannot add log", task_name)
            return

        summary_parts = [f"{key}: {value}" for key, value in details.items()]
        summary = "; ".join(summary_parts)
        payload: dict[str, Any] = {
            "parent": {"page_id": page["id"]},
            "rich_text": [{"type": "text", "text": {"content": summary}}],
        }

        async with AsyncClient(base_url=self.base_url, headers=self._headers) as client:
            response = await client.post("/comments", json=payload)
            try:
                response.raise_for_status()
            except HTTPStatusError as exc:
                logger.error("Failed to log milestone for task '%s': %s", task_name, exc)
                raise

        logger.info("Logged milestone update for task '%s'", task_name)

    async def _find_task_page(self, task_name: str) -> dict[str, Any] | None:
        """Return the first Notion page matching the provided title."""

        if not self.database_id:
            return None

        query_payload = {
            "filter": {
                "property": "Name",
                "title": {
                    "equals": task_name,
                },
            },
            "page_size": 1,
        }

        async with AsyncClient(base_url=self.base_url, headers=self._headers) as client:
            response = await client.post(f"/databases/{self.database_id}/query", json=query_payload)
            try:
                response.raise_for_status()
            except HTTPStatusError as exc:
                logger.error("Failed to query Notion for task '%s': %s", task_name, exc)
                raise

        results = response.json().get("results", [])
        return results[0] if results else None
