from functools import lru_cache

from pydantic import BaseSettings


class AdminSettings(BaseSettings):
    ADMIN_INFINITY_ACCESS_TOKEN: str
    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str
    ADMIN_WORD: str


@lru_cache()
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


class SQLAdminSettings(BaseSettings):
    SQLADMIN_SECRET_KEY: str


@lru_cache()
def get_sqladmin_settings() -> SQLAdminSettings:
    return SQLAdminSettings()


class DatabaseSettings(BaseSettings):
    POT_DATABASE_URI: str


@lru_cache()
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()


class SiteSettings(BaseSettings):
    AUTH_SITE_BASE_URL: str


@lru_cache()
def get_site_settings() -> SiteSettings:
    return SiteSettings()
