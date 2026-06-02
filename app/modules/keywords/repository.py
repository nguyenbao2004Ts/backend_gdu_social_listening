from typing import Any

from prisma import Prisma


class KeywordRepository:
    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def find_all(self) -> list[Any]:
        return await self._db.keyword.find_many(order={"id": "asc"})

    async def find_by_id(self, keyword_id: int) -> Any | None:
        return await self._db.keyword.find_unique(where={"id": keyword_id})

    async def create(self, keyword: str, status: bool) -> Any:
        return await self._db.keyword.create(
            data={"keyword": keyword, "status": status},
        )

    async def update(self, keyword_id: int, data: dict) -> Any:
        return await self._db.keyword.update(where={"id": keyword_id}, data=data)

    async def delete(self, keyword_id: int) -> None:
        await self._db.keyword.delete(where={"id": keyword_id})
