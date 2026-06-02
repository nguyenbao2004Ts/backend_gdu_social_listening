from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str
    app_env: str
    api_v1_prefix: str

    database_url: str
    db_schema: str

    cors_origins: str

    jwt_secret: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    jwt_refresh_token_expire_hours: int

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_development(self) -> bool:
        return self.app_env.lower() in ("development", "dev", "local")


@lru_cache
def get_settings() -> Settings:
    if not _ENV_FILE.exists():
        raise RuntimeError(
            f"Thiếu file .env tại {_ENV_FILE}. Copy từ .env.example và điền giá trị."
        )
    return Settings()
