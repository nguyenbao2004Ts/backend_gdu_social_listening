from collections.abc import AsyncGenerator

from prisma import Prisma

from app.core.prisma import prisma


async def get_prisma() -> AsyncGenerator[Prisma, None]:
    """Inject Prisma client vào Controller."""
    yield prisma
