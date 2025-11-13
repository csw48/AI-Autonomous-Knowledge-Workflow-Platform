from uuid import UUID

from pydantic import BaseModel


class DocumentIngestResponse(BaseModel):
    id: UUID
    title: str
    chunk_count: int
    source: str | None = None
