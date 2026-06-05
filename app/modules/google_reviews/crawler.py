"""Lấy review từ Google Places API (New) — tối đa 5 review/request."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

import httpx
from fastapi import HTTPException, status

PLACES_BASE = "https://places.googleapis.com/v1"

GOOGLE_SETUP_HINT = (
    "Google Places API (New) trả PERMISSION_DENIED. "
    "Bạn đã bật API + restrict key đúng — thường còn 1 trong 3 nguyên nhân sau: "
    "(A) Project Google Cloud chưa gắn Billing account (Billing → Link a billing account); "
    "(B) API key trong .env **không phải** key của đúng project đã bật Places API (copy lại từ Credentials); "
    "(C) Key cũ tạo trước khi bật API → tạo **API key mới** rồi dán vào .env, restart server."
)


@dataclass
class FetchedGoogleReview:
    google_review_id: str
    reviewer: str | None
    rating: int | None
    review_content: str | None
    review_time: datetime | None
    image_url: str | None


class GooglePlacesCrawler:
    def __init__(
        self,
        api_key: str,
        place_id: str,
        text_query: str,
    ) -> None:
        self._api_key = api_key
        self._place_id = place_id.strip()
        self._text_query = text_query.strip()

    def _headers(self, field_mask: str) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._api_key,
            "X-Goog-FieldMask": field_mask,
        }

    @staticmethod
    def _raise_google_error(resp: httpx.Response, context: str) -> None:
        if resp.status_code == 403:
            google_msg = resp.text.strip().replace("\n", " ")[:300]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{GOOGLE_SETUP_HINT} [{context}] {google_msg}",
            )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Google Places {context} lỗi ({resp.status_code}): {resp.text}",
        )

    async def _resolve_place_id(self, client: httpx.AsyncClient) -> str:
        if self._place_id:
            return self._place_id.removeprefix("places/")

        if not self._text_query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cấu hình GOOGLE_MAPS_PLACE_ID hoặc GOOGLE_MAPS_TEXT_QUERY",
            )

        resp = await client.post(
            f"{PLACES_BASE}/places:searchText",
            headers=self._headers("places.id,places.displayName"),
            json={"textQuery": self._text_query, "pageSize": 1},
            timeout=30.0,
        )
        if resp.status_code != 200:
            self._raise_google_error(resp, "searchText")

        places = resp.json().get("places") or []
        if not places:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy địa điểm trên Google Maps",
            )
        pid = places[0].get("id") or ""
        return pid.removeprefix("places/")

    @staticmethod
    def _parse_publish_time(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            normalized = value.replace("Z", "+00:00")
            return datetime.fromisoformat(normalized)
        except ValueError:
            return None

    @staticmethod
    def _parse_review(raw: dict) -> FetchedGoogleReview:
        author = raw.get("authorAttribution") or {}
        text_obj = raw.get("text") or {}
        photos = raw.get("photos") or []
        image_url = None
        if photos:
            image_url = (
                photos[0].get("authorAttributions", [{}])[0].get("photoUri")
                or photos[0].get("googleMapsUri")
            )

        return FetchedGoogleReview(
            google_review_id=raw.get("name") or "",
            reviewer=author.get("displayName"),
            rating=raw.get("rating"),
            review_content=text_obj.get("text"),
            review_time=GooglePlacesCrawler._parse_publish_time(raw.get("publishTime")),
            image_url=image_url,
        )

    async def fetch_reviews(self) -> tuple[str, list[FetchedGoogleReview]]:
        async with httpx.AsyncClient() as client:
            place_id = await self._resolve_place_id(client)
            resp = await client.get(
                f"{PLACES_BASE}/places/{place_id}",
                headers=self._headers("id,reviews"),
                timeout=30.0,
            )
            if resp.status_code != 200:
                self._raise_google_error(resp, "details")

            reviews_raw = resp.json().get("reviews") or []
            parsed = [
                self._parse_review(r)
                for r in reviews_raw
                if r.get("name")
            ]
            return place_id, parsed
