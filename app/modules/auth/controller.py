from fastapi import APIRouter, Depends
from prisma import Prisma

from app.core.config import Settings, get_settings
from app.core.deps import get_prisma
from app.core.security import get_current_user
from app.schemas.auth import CurrentUser
from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService
from app.modules.users.repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from app.schemas.users import UserProfile
from app.modules.users.service import UserService

router = APIRouter()


def _get_service(
    db: Prisma = Depends(get_prisma),
    settings: Settings = Depends(get_settings),
) -> AuthService:
    user_repo = UserRepository(db)
    return AuthService(
        AuthRepository(user_repo),
        UserService(user_repo),
        settings,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    service: AuthService = Depends(_get_service),
) -> TokenResponse:
    return await service.login(body)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_tokens(
    body: RefreshRequest,
    service: AuthService = Depends(_get_service),
) -> TokenResponse:
    """Đổi refresh_token lấy access_token + refresh_token mới."""
    return await service.refresh(body)


@router.post("/register", response_model=UserProfile, status_code=201)
async def register(
    body: RegisterRequest,
    service: AuthService = Depends(_get_service),
) -> UserProfile:
    """Tạo tài khoản mới — không cần JWT. role: marketing | hr | admissions."""
    return await service.register(body)


@router.get("/profile", response_model=UserProfile)
async def profile(
    current_user: CurrentUser = Depends(get_current_user),
    service: AuthService = Depends(_get_service),
) -> UserProfile:
    return await service.get_profile(current_user.username)
