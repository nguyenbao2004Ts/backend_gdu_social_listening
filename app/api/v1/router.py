from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.modules.auth.controller import router as auth_router
from app.modules.health.controller import router as health_router
from app.modules.keywords.controller import router as keywords_router
from app.modules.users.controller import router as users_router

api_router = APIRouter()

# Public — không cần JWT
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# Protected — Swagger hiện ổ khóa, gọi API phải Bearer token
_protected = [Depends(get_current_user)]
api_router.include_router(
    users_router,
    prefix="/users",
    tags=["Users"],
    dependencies=_protected,
)
api_router.include_router(
    keywords_router,
    prefix="/keywords",
    tags=["Keywords"],
    dependencies=_protected,
)
