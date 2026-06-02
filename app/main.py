from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.middleware.api_log import ApiLogMiddleware
from app.core.prisma import connect_prisma, disconnect_prisma


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await connect_prisma()
    yield
    await disconnect_prisma()


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description=(
            "API GDU Social Listening — thu thập & báo cáo mention GDU. "
            "Swagger: **/docs** | ReDoc: **/redoc**"
        ),
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ApiLogMiddleware)

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.get("/", tags=["Root"])
    async def root() -> dict:
        return {
            "message": settings.app_name,
            "docs": "/docs",
            "health": f"{settings.api_v1_prefix}/health",
        }

    return app


app = create_app()
