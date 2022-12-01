from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_database_settings

_engine: AsyncEngine = create_async_engine(
    get_database_settings().USER_DATABASE_URI, pool_pre_ping=True
)
session = sessionmaker(class_=AsyncSession, bind=_engine, autocommit=False, autoflush=False)
