from prisma import Prisma


class HealthRepository:
    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def count_app_users(self) -> int:
        return await self._db.appuser.count()
