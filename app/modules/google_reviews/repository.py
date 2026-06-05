from datetime import UTC, datetime
from typing import Any

from prisma import Prisma


class GoogleReviewRepository:
    def __init__(self, db: Prisma) -> None:
        self._db = db

    async def find_all(self, skip: int = 0, limit: int = 100) -> list[Any]:
        return await self._db.googlereview.find_many(
            skip=skip,
            take=limit,
            order={"reviewTime": "desc"},
        )

    async def count_all(self) -> int:
        return await self._db.googlereview.count()

    async def find_by_google_review_id(self, google_review_id: str) -> Any | None:
        return await self._db.googlereview.find_unique(
            where={"googleReviewId": google_review_id},
        )

    async def create(self, data: dict) -> Any:
        return await self._db.googlereview.create(data=data)

    async def update(self, review_id: int, data: dict) -> Any:
        return await self._db.googlereview.update(
            where={"id": review_id},
            data=data,
        )

    async def create_crawl_log(
        self,
        source_name: str,
        status: str,
        total_records: int,
        finished_at: datetime | None = None,
    ) -> Any:
        return await self._db.crawllog.create(
            data={
                "sourceName": source_name,
                "status": status,
                "totalRecords": total_records,
                "finishedAt": finished_at or datetime.now(UTC),
            },
        )
