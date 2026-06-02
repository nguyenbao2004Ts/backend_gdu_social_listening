from typing import Any

from prisma import Prisma


class UserRepository:
    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def find_all(self) -> list[Any]:
        return await self._db.appuser.find_many(order={"id": "asc"})

    async def find_by_username(self, username: str) -> Any | None:
        return await self._db.appuser.find_unique(where={"username": username})

    async def create(self, data: dict) -> Any:
        return await self._db.appuser.create(data=data)
