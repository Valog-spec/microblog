import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Конфигурация приложения"""

    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT")
    model_config = SettingsConfigDict(env_file=ENV_PATH)


@lru_cache
def get_app_settings() -> Settings:
    """
    Возвращает экземпляр настроек приложения с кэшированием.

    Returns:
        Settings: Экземпляр класса настроек приложения
    """

    return Settings()


def get_settings_no_cache() -> Settings:
    """
    Возвращает экземпляр настроек приложения без кэширования.

    Returns:
        Settings: Экземпляр класса настроек приложения
    """
    return Settings()
