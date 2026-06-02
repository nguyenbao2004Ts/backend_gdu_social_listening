from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# .env cùng thư mục gốc project (gdu_social_listerning)
_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE) if _ENV_FILE.exists() else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "GDU Social Listening API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"

    database_url: str
    db_schema: str = "dev"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in ("development", "dev", "local")


@lru_cache
def get_settings() -> Settings:
    return Settings()
