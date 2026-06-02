from fastapi import APIRouter, Depends
from prisma import Prisma

from app.core.deps import get_prisma
from app.modules.users.repository import UserRepository
from app.schemas.users import UserProfile
from app.modules.users.service import UserService

router = APIRouter()


def _get_service(db: Prisma = Depends(get_prisma)) -> UserService:
    return UserService(UserRepository(db))


@router.get("", response_model=list[UserProfile])
async def list_users(service: UserService = Depends(_get_service)) -> list[UserProfile]:
    return await service.list_users()
