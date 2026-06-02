import logging
import time
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import get_settings
from app.core.prisma import prisma
from app.core.security import decode_token_user_id
from app.modules.api_logs.repository import ApiLogRepository

logger = logging.getLogger(__name__)

MAX_BODY_CHARS = 8000

# Không ghi log (tránh rác / vòng lặp)
SKIP_LOG_PREFIXES = (
    "/docs",
    "/redoc",
    "/openapi.json",
    "/favicon.ico",
)


def _truncate(text: str | None) -> str | None:
    if text is None:
        return None
    if len(text) <= MAX_BODY_CHARS:
        return text
    return text[:MAX_BODY_CHARS] + "...(truncated)"


def _decode_body(raw: bytes) -> str | None:
    if not raw:
        return None
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return "<binary>"


class ApiLogMiddleware(BaseHTTPMiddleware):
    """Mỗi request API → 1 dòng trong dev.API_LOGS."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        path = request.url.path
        if path == "/" or any(path.startswith(p) for p in SKIP_LOG_PREFIXES):
            return await call_next(request)

        settings = get_settings()
        start = time.perf_counter()

        body_bytes = await request.body()

        async def receive() -> dict:
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        request = Request(request.scope, receive)

        response = await call_next(request)

        resp_chunks: list[bytes] = []
        async for chunk in response.body_iterator:
            resp_chunks.append(chunk)
        resp_bytes = b"".join(resp_chunks)

        duration_ms = (time.perf_counter() - start) * 1000
        auth_header = request.headers.get("authorization", "")
        token = auth_header.removeprefix("Bearer ").strip() if auth_header else None
        user_id = decode_token_user_id(token, settings)

        name_log = f"{request.method} {path}"
        input_str = _truncate(_decode_body(body_bytes))
        output_str = _truncate(_decode_body(resp_bytes))

        try:
            if prisma.is_connected():
                await ApiLogRepository(prisma).create(
                    name_log=name_log,
                    request_method=request.method,
                    request_url=str(request.url),
                    input_data=input_str,
                    output_data=output_str,
                    user_create=user_id,
                    status_code=response.status_code,
                    execution_time=f"{duration_ms:.2f}ms",
                )
        except Exception:
            logger.exception("Không ghi được API_LOGS: %s", name_log)

        return Response(
            content=resp_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
