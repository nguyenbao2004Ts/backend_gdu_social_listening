from typing import Any

from fastapi import HTTPException

from app.modules.keywords.repository import KeywordRepository
from app.schemas.keywords import KeywordCreate, KeywordResponse, KeywordUpdate


def _to_response(row: Any) -> KeywordResponse:
    return KeywordResponse(
        id=int(row.id),
        keyword=row.keyword,
        status=row.status,
        created_at=row.createdAt,
    )


class KeywordService:
    def __init__(self, repo: KeywordRepository) -> None:
        self._repo = repo

    async def list_keywords(self) -> list[KeywordResponse]:
        rows = await self._repo.find_all()
        return [_to_response(r) for r in rows]

    async def create(self, body: KeywordCreate) -> KeywordResponse:
        row = await self._repo.create(body.keyword, body.status)
        return _to_response(row)

    async def update(self, keyword_id: int, body: KeywordUpdate) -> KeywordResponse:
        existing = await self._repo.find_by_id(keyword_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Keyword không tồn tại")

        data: dict = {}
        if body.keyword is not None:
            data["keyword"] = body.keyword
        if body.status is not None:
            data["status"] = body.status

        row = await self._repo.update(keyword_id, data)
        return _to_response(row)

    async def delete(self, keyword_id: int) -> None:
        existing = await self._repo.find_by_id(keyword_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Keyword không tồn tại")
        await self._repo.delete(keyword_id)
