from fastapi import APIRouter, Depends
from prisma import Prisma

from app.core.deps import get_prisma
from app.modules.keywords.repository import KeywordRepository
from app.schemas.keywords import KeywordCreate, KeywordResponse, KeywordUpdate
from app.modules.keywords.service import KeywordService

router = APIRouter()


def _get_service(db: Prisma = Depends(get_prisma)) -> KeywordService:
    return KeywordService(KeywordRepository(db))


@router.get("", response_model=list[KeywordResponse])
async def list_keywords(
    service: KeywordService = Depends(_get_service),
) -> list[KeywordResponse]:
    return await service.list_keywords()


@router.post("", response_model=KeywordResponse, status_code=201)
async def create_keyword(
    body: KeywordCreate,
    service: KeywordService = Depends(_get_service),
) -> KeywordResponse:
    return await service.create(body)


@router.put("/{keyword_id}", response_model=KeywordResponse)
async def update_keyword(
    keyword_id: int,
    body: KeywordUpdate,
    service: KeywordService = Depends(_get_service),
) -> KeywordResponse:
    return await service.update(keyword_id, body)


@router.delete("/{keyword_id}", status_code=204)
async def delete_keyword(
    keyword_id: int,
    service: KeywordService = Depends(_get_service),
) -> None:
    await service.delete(keyword_id)
