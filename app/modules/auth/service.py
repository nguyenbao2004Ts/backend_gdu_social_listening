from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import Settings
from app.modules.auth.repository import AuthRepository
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.users import UserProfile
from app.modules.users.service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Đăng ký tự do — không cho tạo admin qua API public
REGISTER_ROLES = frozenset({"marketing", "hr", "admissions"})


class AuthService:
    def __init__(
        self,
        repo: AuthRepository,
        user_service: UserService,
        settings: Settings,
    ) -> None:
        self._repo = repo
        self._user_service = user_service
        self._settings = settings

    def _create_access_token(self, user) -> str:
        expire = datetime.now(UTC) + timedelta(
            minutes=self._settings.jwt_access_token_expire_minutes
        )
        payload = {
            "sub": user.username,
            "user_id": int(user.id),
            "role": user.role,
            "type": "access",
            "exp": expire,
        }
        return jwt.encode(
            payload,
            self._settings.jwt_secret,
            algorithm=self._settings.jwt_algorithm,
        )

    def _create_refresh_token(self, user) -> str:
        expire = datetime.now(UTC) + timedelta(
            hours=self._settings.jwt_refresh_token_expire_hours
        )
        payload = {
            "sub": user.username,
            "user_id": int(user.id),
            "type": "refresh",
            "exp": expire,
        }
        return jwt.encode(
            payload,
            self._settings.jwt_secret,
            algorithm=self._settings.jwt_algorithm,
        )

    def _issue_tokens(self, user) -> TokenResponse:
        return TokenResponse(
            access_token=self._create_access_token(user),
            expires_in=self._settings.jwt_access_token_expire_minutes * 60,
            refresh_token=self._create_refresh_token(user),
            refresh_expires_in=self._settings.jwt_refresh_token_expire_hours * 3600,
        )

    async def login(self, body: LoginRequest) -> TokenResponse:
        user = await self._repo.find_by_username(body.username)
        if user is None or not pwd_context.verify(body.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sai username hoặc password",
            )
        return self._issue_tokens(user)

    async def refresh(self, body: RefreshRequest) -> TokenResponse:
        try:
            payload = jwt.decode(
                body.refresh_token,
                self._settings.jwt_secret,
                algorithms=[self._settings.jwt_algorithm],
            )
        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token hết hạn hoặc không hợp lệ",
            ) from exc

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token không hợp lệ",
            )

        username: str | None = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token không hợp lệ",
            )

        user = await self._repo.find_by_username(username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User không tồn tại",
            )
        return self._issue_tokens(user)

    async def register(self, body: RegisterRequest) -> UserProfile:
        role = body.role.strip().lower()
        if role not in REGISTER_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"role phải là một trong: {', '.join(sorted(REGISTER_ROLES))}",
            )

        existing = await self._repo.find_by_username(body.username)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username đã tồn tại",
            )

        full_name = body.full_name
        if not full_name and (body.first_name or body.last_name):
            parts = [p for p in (body.first_name, body.last_name) if p]
            full_name = " ".join(parts)

        user = await self._user_service.create_user(
            username=body.username,
            password_hash=pwd_context.hash(body.password),
            role=role,
            first_name=body.first_name,
            last_name=body.last_name,
            full_name=full_name,
            sdt=body.sdt,
            sex=body.sex,
        )
        return user

    async def get_profile(self, username: str) -> UserProfile:
        profile = await self._user_service.get_by_username(username)
        if profile is None:
            raise HTTPException(status_code=404, detail="User không tồn tại")
        return profile
