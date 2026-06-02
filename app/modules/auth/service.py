from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.core.config import Settings
from app.modules.auth.repository import AuthRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
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
            "exp": expire,
        }
        return jwt.encode(
            payload,
            self._settings.jwt_secret,
            algorithm=self._settings.jwt_algorithm,
        )

    async def login(self, body: LoginRequest) -> TokenResponse:
        user = await self._repo.find_by_username(body.username)
        if user is None or not pwd_context.verify(body.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Sai username hoặc password",
            )
        token = self._create_access_token(user)
        return TokenResponse(access_token=token)

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
