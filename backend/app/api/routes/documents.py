from __future__ import annotations

from typing import Any

from backend.app.api.dependencies import get_db
from backend.app.models.schemas.documents import DocumentIngestResponse
from backend.app.services.documents import DocumentService
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentIngestResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    source: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
) -> DocumentIngestResponse:
    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or unreadable.")

    service = DocumentService(db)
    try:
        document = await service.ingest_file(
            filename=file.filename or "upload",
            content_type=file.content_type,
            data=raw,
            title=title,
            source=source,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return DocumentIngestResponse(
        id=document.id,
        title=document.title,
        source=document.source,
        chunk_count=len(document.chunks),
    )
