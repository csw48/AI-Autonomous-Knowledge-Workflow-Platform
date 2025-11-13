from __future__ import annotations

from backend.app.models.db.documents import DocumentChunk
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession


class SearchService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(self, query: str, limit: int = 5) -> list[dict[str, str]]:
        stmt = (
            select(DocumentChunk)
            .where(func.lower(DocumentChunk.content).contains(query.lower()))
            .order_by(DocumentChunk.chunk_index)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [
            {
                "document_id": str(chunk.document_id),
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk in result.scalars().all()
        ]
