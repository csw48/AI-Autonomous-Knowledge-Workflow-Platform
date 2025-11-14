from __future__ import annotations

import re

from backend.app.models.db.documents import DocumentChunk
from backend.app.services.embeddings import EmbeddingService
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


class SearchService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(self, query: str, limit: int = 5) -> list[dict[str, str]]:
        """Keyword-based search over chunk content.

        - Rozbije dopyt na tokeny (slová >= 3 znaky).
        - Vyberie chunky, ktoré obsahujú aspoň jeden token.
        - Výsledky zoradí podľa počtu nájdených tokenov (desc), potom podľa indexu chunku.
        """

        normalized_query = query.strip().lower()
        tokens = {t for t in re.split(r"\W+", normalized_query) if len(t) >= 3}

        stmt = select(DocumentChunk)
        if tokens:
            conditions = [
                func.lower(DocumentChunk.content).contains(token) for token in tokens
            ]
            stmt = stmt.where(or_(*conditions))
        elif normalized_query:
            stmt = stmt.where(
                func.lower(DocumentChunk.content).contains(normalized_query)
            )
        else:
            return []

        result = await self.session.execute(stmt)
        chunks = list(result.scalars().all())

        def score(chunk: DocumentChunk) -> int:
            text = chunk.content.lower()
            return sum(1 for token in tokens if token in text) or 0

        chunks.sort(key=lambda c: (-score(c), c.chunk_index))
        chunks = chunks[:limit]

        return [
            {
                "document_id": str(chunk.document_id),
                "chunk_index": chunk.chunk_index,
                "content": chunk.content,
            }
            for chunk in chunks
        ]

    async def search_by_vector(self, query: str, limit: int = 5) -> list[dict[str, str]]:
        """Vector-based search over chunk embeddings with graceful fallback."""

        embedder = EmbeddingService()
        query_vector = (await embedder.embed([query]))[0]

        try:
            distance_expr = DocumentChunk.embedding.l2_distance(query_vector)  # type: ignore[attr-defined]
        except AttributeError:  # pragma: no cover - non-pgvector backends
            return await self.search(query=query, limit=limit)

        stmt = (
            select(DocumentChunk)
            .where(DocumentChunk.embedding.isnot(None))
            .order_by(distance_expr)
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
