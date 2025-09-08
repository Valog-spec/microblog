import asyncio
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.dependencies import get_db
from app.database.database import Base
from app.main import app
from app.models.tweet import Tweet
from app.models.user import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

AsyncTestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Создает event loop для тестовой сессии."""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    """Создает и удаляет таблицы для каждого теста."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Создает сессию БД для каждого теста."""
    async with AsyncTestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(scope="function")
async def test_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Создает асинхронного тестового клиента."""

    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Создает и возвращает тестового пользователя."""
    user = User(name="testuser", api_key="test_api_key")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_tweet(db_session: AsyncSession, test_user: User) -> Tweet:
    """Создает и возвращает тестовый твит."""
    tweet = Tweet(content="Test tweet", author_id=test_user.id)
    db_session.add(tweet)
    await db_session.commit()
    await db_session.refresh(tweet)
    return tweet
