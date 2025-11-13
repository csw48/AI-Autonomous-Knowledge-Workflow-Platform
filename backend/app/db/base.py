from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


# Import models for metadata registration
from backend.app.models.db.documents import Document, DocumentChunk  # noqa: E402,F401
