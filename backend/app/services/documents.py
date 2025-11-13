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
        await self.session.commit()
        await self.session.refresh(document)
        return document

    async def list_documents(self) -> list[Document]:
        stmt = select(Document).options(selectinload(Document.chunks))
        result = await self.session.execute(stmt)
        return list(result.scalars())
