from fastapi import APIRouter, Depends
from prisma import Prisma

from app.core.config import Settings, get_settings
from app.core.deps import get_prisma
from app.modules.health.repository import HealthRepository
from app.modules.health.service import HealthService

router = APIRouter()


def _get_service(
    db: Prisma = Depends(get_prisma),
    settings: Settings = Depends(get_settings),
) -> HealthService:
    return HealthService(HealthRepository(db), settings)


@router.get("/health")
async def health_check(service: HealthService = Depends(_get_service)) -> dict:
    """Kiểm tra API + PostgreSQL."""
    return await service.get_status()
