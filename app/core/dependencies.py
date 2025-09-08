from typing import Annotated, AsyncGenerator

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import AsyncSessionLocal
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.like_service import LikeService
from app.services.media_service import MediaService
from app.services.tweet_service import TweetService
from app.services.user_service import UserService


async def get_db() -> AsyncGenerator:
    """Создает и возвращает асинхронную сессию базы данных"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_current_user(
    api_key: str = Header(..., alias="api-key"), db: AsyncSession = Depends(get_db)
) -> User:
    """Аутентифицирует пользователя по API ключу из заголовка запроса"""
    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_api_key(api_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return user


async def get_tweet_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TweetService:
    """Создает и возвращает сервис для работы с твитами"""
    return TweetService(db)


async def get_media_service(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MediaService:
    """Создает и возвращает сервис для работы с медиафайлами"""
    return MediaService(db)


async def get_like_service(db: Annotated[AsyncSession, Depends(get_db)]) -> LikeService:
    """Создает и возвращает сервис для работы с лайками"""
    return LikeService(db)


async def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]) -> UserService:
    """Создает и возвращает сервис для работы с пользователями"""
    return UserService(db_session=db)
