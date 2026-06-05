from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, status

from app.core.config import Settings
from app.modules.google_reviews.crawler import GooglePlacesCrawler
from app.modules.google_reviews.repository import GoogleReviewRepository
from app.schemas.google_reviews import GoogleReviewCrawlResponse, GoogleReviewResponse


def _to_response(row: Any) -> GoogleReviewResponse:
    return GoogleReviewResponse(
        id=int(row.id),
        google_review_id=row.googleReviewId,
        reviewer=row.reviewer,
        rating=row.rating,
        review_content=row.reviewContent,
        review_time=row.reviewTime,
        image_url=row.imageUrl,
    )


class GoogleReviewService:
    def __init__(self, repo: GoogleReviewRepository, settings: Settings) -> None:
        self._repo = repo
        self._settings = settings

    def _crawler(self) -> GooglePlacesCrawler:
        if not self._settings.google_places_api_key.strip():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Chưa cấu hình GOOGLE_PLACES_API_KEY trong .env",
            )
        return GooglePlacesCrawler(
            api_key=self._settings.google_places_api_key,
            place_id=self._settings.google_maps_place_id,
            text_query=self._settings.google_maps_text_query,
        )

    async def _upsert_review(self, item) -> tuple[bool, Any]:
        """Trả (is_new, row)."""
        existing = await self._repo.find_by_google_review_id(item.google_review_id)
        data = {
            "googleReviewId": item.google_review_id,
            "reviewer": item.reviewer,
            "rating": item.rating,
            "reviewContent": item.review_content,
            "reviewTime": item.review_time,
            "imageUrl": item.image_url,
        }
        if existing is None:
            row = await self._repo.create(data)
            return True, row
        row = await self._repo.update(int(existing.id), data)
        return False, row

    async def crawl_and_list(self) -> GoogleReviewCrawlResponse:
        crawler = self._crawler()
        source = self._settings.google_maps_url or "Google Maps — GDU"

        try:
            place_id, fetched = await crawler.fetch_reviews()
            imported = 0
            updated = 0
            saved_rows: list[Any] = []

            for item in fetched:
                is_new, row = await self._upsert_review(item)
                if is_new:
                    imported += 1
                else:
                    updated += 1
                saved_rows.append(row)

            total = await self._repo.count_all()
            await self._repo.create_crawl_log(
                source_name=source,
                status="success",
                total_records=len(fetched),
            )

            return GoogleReviewCrawlResponse(
                place_id=place_id,
                imported=imported,
                updated=updated,
                total_in_db=total,
                reviews=[_to_response(r) for r in saved_rows],
            )
        except HTTPException:
            await self._repo.create_crawl_log(
                source_name=source,
                status="failed",
                total_records=0,
            )
            raise
        except Exception as exc:
            await self._repo.create_crawl_log(
                source_name=source,
                status="failed",
                total_records=0,
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Crawl Google Review thất bại: {exc}",
            ) from exc

    async def list_reviews(self, skip: int = 0, limit: int = 100) -> list[GoogleReviewResponse]:
        rows = await self._repo.find_all(skip=skip, limit=limit)
        return [_to_response(r) for r in rows]
