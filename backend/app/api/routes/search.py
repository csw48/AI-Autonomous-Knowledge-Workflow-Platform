from backend.app.api.dependencies import get_db
from backend.app.services.search import SearchService
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    document_id: str
    chunk_index: int
    content: str


@router.post("", response_model=list[SearchResult])
async def search_chunks(
    payload: SearchRequest, db: AsyncSession = Depends(get_db)
) -> list[SearchResult]:
    service = SearchService(db)
    matches = await service.search(query=payload.query, limit=payload.limit)
    return [SearchResult(**match) for match in matches]
