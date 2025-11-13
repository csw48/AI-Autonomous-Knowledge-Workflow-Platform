"""Helper CLI to update Notion task statuses."""

# ruff: noqa: E402

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from backend.app.integrations.notion import NotionClient


async def _run(task: str, status: str, details: list[str]) -> None:
    client = NotionClient()
    await client.update_task_status(task, status)

    if details:
        detail_map: dict[str, Any] = {
            f"note_{i}": value for i, value in enumerate(details, start=1)
        }
        await client.log_milestone(task, detail_map)


def main() -> None:
    parser = argparse.ArgumentParser(description="Update a Notion Kanban item status")
    parser.add_argument("task", help="Exact name of the Notion task")
    parser.add_argument("status", help="Target status (To Do, In Progress, Done)")
    parser.add_argument(
        "--note",
        action="append",
        default=[],
        help="Optional note to log alongside the status update (can be repeated)",
    )

    args = parser.parse_args()
    asyncio.run(_run(args.task, args.status, args.note))


if __name__ == "__main__":
    main()
