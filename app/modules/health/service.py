from app.core.config import Settings
from app.modules.health.repository import HealthRepository


class HealthService:
    def __init__(self, repo: HealthRepository, settings: Settings) -> None:
        self._repo = repo
        self._settings = settings

    async def get_status(self) -> dict:
        user_count = await self._repo.count_app_users()
        return {
            "status": "ok",
            "app": self._settings.app_name,
            "env": self._settings.app_env,
            "db_schema": self._settings.db_schema,
            "app_user_count": user_count,
        }
