"""
Pydantic DTO — request/response API (dùng chung, import vào module).

Ví dụ:
    from app.schemas.auth import LoginRequest
    from app.schemas.users import UserProfile
"""

from app.schemas.auth import CurrentUser, LoginRequest, RegisterRequest, TokenResponse
from app.schemas.keywords import KeywordCreate, KeywordResponse, KeywordUpdate
from app.schemas.users import UserProfile

__all__ = [
    "CurrentUser",
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "UserProfile",
    "KeywordCreate",
    "KeywordUpdate",
    "KeywordResponse",
]
