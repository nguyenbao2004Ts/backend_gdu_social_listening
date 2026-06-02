from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from prisma import Prisma

from app.core.config import Settings, get_settings
from app.core.deps import get_prisma
from app.modules.users.repository import UserRepository
from app.schemas.auth import CurrentUser

# Swagger Authorize — một scheme duy nhất (BearerAuth)
http_bearer = HTTPBearer(
    auto_error=True,
    scheme_name="BearerAuth",
    bearerFormat="JWT",
    description="POST /api/v1/auth/login lấy token, dán vào Authorize",
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Prisma = Depends(get_prisma),
    settings: Settings = Depends(get_settings),
) -> CurrentUser:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        if payload.get("type") == "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Use access token",
            )

        username: str | None = payload.get("sub")
        user_id = payload.get("user_id")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ",
            )
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token hết hạn hoặc không hợp lệ",
        ) from exc

    if user_id is not None:
        return CurrentUser(id=int(user_id), username=username, role=payload.get("role", ""))

    user = await UserRepository(db).find_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User không tồn tại",
        )
    return CurrentUser(id=int(user.id), username=user.username, role=user.role)


def decode_token_user_id(
    token: str | None,
    settings: Settings,
) -> int | None:
    """Đọc user_id từ Bearer token (middleware log — không raise)."""
    if not token:
        return None
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        uid = payload.get("user_id")
        return int(uid) if uid is not None else None
    except (JWTError, TypeError, ValueError):
        return None
