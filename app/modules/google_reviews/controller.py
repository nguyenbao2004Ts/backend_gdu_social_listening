from fastapi import APIRouter, Depends, Query
from prisma import Prisma

from app.core.config import Settings, get_settings
from app.core.deps import get_prisma
from app.modules.google_reviews.repository import GoogleReviewRepository
from app.modules.google_reviews.service import GoogleReviewService
from app.schemas.google_reviews import GoogleReviewCrawlResponse, GoogleReviewResponse

router = APIRouter()


def _get_service(
    db: Prisma = Depends(get_prisma),
    settings: Settings = Depends(get_settings),
) -> GoogleReviewService:
    return GoogleReviewService(GoogleReviewRepository(db), settings)


@router.get("", response_model=list[GoogleReviewResponse])
async def list_google_reviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    service: GoogleReviewService = Depends(_get_service),
) -> list[GoogleReviewResponse]:
    """Danh sách review đã lưu trong DB."""
    return await service.list_reviews(skip=skip, limit=limit)


@router.post("/crawl", response_model=GoogleReviewCrawlResponse)
async def crawl_google_reviews(
    service: GoogleReviewService = Depends(_get_service),
) -> GoogleReviewCrawlResponse:
    """
    Gọi Google Places API → lưu/ cập nhật DB → trả dữ liệu vừa crawl.

    Lưu ý: API chính thức trả tối đa **5** review mỗi lần (giới hạn Google).
    """
    return await service.crawl_and_list()
