from functools import lru_cache

from pydantic import BaseSettings


class AdminSettings(BaseSettings):
    ADMIN_INFINITY_ACCESS_TOKEN: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class DatabaseSettings(BaseSettings):
    POKER_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class SiteSettings(BaseSettings):
    AUTH_SITE_BASE_URL: str
    CHAT_SITE_BASE_URL: str


@lru_cache()
def get_site_settings() -> SiteSettings:
    return SiteSettings()
