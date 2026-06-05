from datetime import datetime

from pydantic import BaseModel, Field


class GoogleReviewResponse(BaseModel):
    id: int
    google_review_id: str | None
    reviewer: str | None
    rating: int | None
    review_content: str | None
    review_time: datetime | None
    image_url: str | None

    model_config = {"from_attributes": True}


class GoogleReviewCrawlResponse(BaseModel):
    place_id: str
    imported: int
    updated: int
    total_in_db: int
    reviews: list[GoogleReviewResponse]
