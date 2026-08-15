from __future__ import annotations
from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    bot_token: str
    group_id: str
    
    vk_token: str | None = None
    vk_group_id: int = 0
    vk_chat_peer_id: int = 0
    vk_api_version: str = "5.199"

    admin_ids: str = ""
    developer_id: int = 620159705
    curator_id: int = 1331701095

    logs_secret_key: str = ""

    api_keys: str = ""

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_days: int = 30

    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432

    show_docs: bool = False

    @computed_field
    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def admin_ids_list(self) -> list[int]:
        return [int(x.strip()) for x in self.admin_ids.split(",") if x.strip()]

    @computed_field
    @property
    def api_keys_list(self) -> list[str]:
        return [k.strip() for k in self.api_keys.split(";") if k.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
