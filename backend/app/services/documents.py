from __future__ import annotations

from collections.abc import Sequence

from backend.app.models.db.documents import Document, DocumentChunk
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


class DocumentService:
    """Persistence helper for documents and their vector representations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def ingest_text(
        self,
        *,
        title: str,
        source: str | None,
        content: str,
        meta: dict | None = None,
        chunk_size: int = 800,
        chunk_overlap: int = 80,
    ) -> Document:
        chunks = self._chunk_text(content, chunk_size=chunk_size, overlap=chunk_overlap)
        if not chunks:
            raise ValueError("Document must contain readable text.")

        return await self.create_document(
            title=title,
            source=source,
            meta=meta,
            chunks=chunks,
            embeddings=None,
        )

    async def create_document(
        self,
        *,
        title: str,
        source: str | None = None,
        meta: dict | None = None,
        chunks: Sequence[str],
        embeddings: Sequence[Sequence[float]] | None = None,
    ) -> Document:
        document = Document(title=title, source=source, meta=meta or {})

        for idx, chunk_text in enumerate(chunks):
            embedding = None
            if embeddings is not None and idx < len(embeddings):
                embedding = list(embeddings[idx])

            document.chunks.append(
                DocumentChunk(chunk_index=idx, content=chunk_text, embedding=embedding)
            )

        self.session.add(document)
        await self.session.flush()
        await self.session.commit()
        return document

    async def list_documents(self) -> list[Document]:
        stmt = select(Document).options(selectinload(Document.chunks))
        result = await self.session.execute(stmt)
        return list(result.scalars())

    @staticmethod
    def _chunk_text(content: str, *, chunk_size: int = 800, overlap: int = 80) -> list[str]:
        normalized = content.replace("\r\n", "\n").strip()
        if not normalized:
            return []

        overlap = max(0, min(overlap, chunk_size // 2))
        chunks: list[str] = []
        start = 0
        text_length = len(normalized)

        while start < text_length:
            end = min(text_length, start + chunk_size)
            chunk = normalized[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end == text_length:
                break
            start = max(end - overlap, start + 1)

        return chunks
