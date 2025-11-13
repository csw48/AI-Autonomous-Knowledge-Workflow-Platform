from __future__ import annotations

from typing import Any

from backend.app.api.dependencies import get_db
from backend.app.models.schemas.documents import DocumentIngestResponse
from backend.app.services.documents import DocumentService
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/documents", tags=["documents"])


async def _read_text_payload(file: UploadFile) -> str:
    raw = await file.read()
    if not raw:
        return ""

    encodings = ["utf-8", "latin-1"]
    for encoding in encodings:
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue

    return raw.decode("utf-8", errors="ignore")


@router.post("", response_model=DocumentIngestResponse)
async def upload_document(
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
    source: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
) -> DocumentIngestResponse:
    text = (await _read_text_payload(file)).strip()
    if not text:
        raise HTTPException(status_code=400, detail="Uploaded file is empty or unreadable.")

    inferred_title = title or file.filename or "Untitled"
    inferred_source = source or file.filename

    meta: dict[str, Any] = {
        "content_type": file.content_type,
        "filename": file.filename,
    }

    service = DocumentService(db)
    try:
        document = await service.ingest_text(
            title=inferred_title,
            source=inferred_source,
            content=text,
            meta=meta,
        )
    except ValueError as exc:  # pragma: no cover - defensive branch
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return DocumentIngestResponse(
        id=document.id,
        title=document.title,
        source=document.source,
        chunk_count=len(document.chunks),
    )
