from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID as UUIDType
from uuid import uuid4

from sqlalchemy import JSON, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


def vector_column(dimensions: int | None = None):
    try:
        from pgvector.sqlalchemy import Vector  # type: ignore

        return Vector(dimensions=dimensions)
    except Exception:  # pragma: no cover - fallback for local dev without pgvector
        return JSON


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255))
    source: Mapped[str | None] = mapped_column(String(255), nullable=True)
    meta: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    __table_args__ = (Index("ix_document_chunks_document_id", "document_id"),)

    id: Mapped[UUIDType] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id: Mapped[UUIDType] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )
    chunk_index: Mapped[int] = mapped_column()
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[Any | None] = mapped_column(vector_column(1536), nullable=True)

    document: Mapped[Document] = relationship(back_populates="chunks")
