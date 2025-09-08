from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_app_settings

app_settings = get_app_settings()

DATABASE_URL = (f"postgresql+asyncpg://{app_settings.POSTGRES_USER}:{app_settings.POSTGRES_PASSWORD}@"
                f"{app_settings.POSTGRES_HOST}:{app_settings.POSTGRES_PORT}/{app_settings.POSTGRES_DB}")
print(DATABASE_URL)
# DATABASE_URL = "sqlite+aiosqlite:///mydb.db"


engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass

