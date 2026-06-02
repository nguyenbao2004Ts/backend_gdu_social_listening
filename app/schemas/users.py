from pydantic import BaseModel


class UserProfile(BaseModel):
    """DTO trả về API — không có password."""

    id: int
    username: str
    role: str
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    sdt: str | None = None
    avatar_url: str | None = None
    sex: str | None = None

    model_config = {"from_attributes": True}
