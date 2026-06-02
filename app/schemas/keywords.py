from datetime import datetime

from pydantic import BaseModel, Field


class KeywordCreate(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=255)
    status: bool = True


class KeywordUpdate(BaseModel):
    keyword: str | None = Field(None, min_length=1, max_length=255)
    status: bool | None = None


class KeywordResponse(BaseModel):
    id: int
    keyword: str
    status: bool
    created_at: datetime

    model_config = {"from_attributes": True}
