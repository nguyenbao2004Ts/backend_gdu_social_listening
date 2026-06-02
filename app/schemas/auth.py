from pydantic import BaseModel, Field


from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    role: str = Field(default="marketing", max_length=50)
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    full_name: str | None = Field(None, max_length=255)
    sdt: str | None = Field(None, max_length=20)
    sex: str | None = Field(None, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CurrentUser(BaseModel):
    """User từ JWT — dùng sau khi đã đăng nhập."""

    id: int
    username: str
    role: str
