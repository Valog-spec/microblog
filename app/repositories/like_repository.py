from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.like import Like


class LikeRepository:
    """Репозиторий для работы с лайками"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_like(self, user_id: int, tweet_id: int) -> Like | None:
        """Поставить лайк на твит по id пользователя и твита"""
        existing_like = await self.get_like(user_id, tweet_id)
        if existing_like:
            return existing_like

        db_like = Like(user_id=user_id, tweet_id=tweet_id)
        self.db_session.add(db_like)
        await self.db_session.commit()
        await self.db_session.refresh(db_like)
        return db_like

    async def delete_like(self, user_id: int, tweet_id: int) -> bool:
        """Удалить лайк с твита"""
        like = await self.get_like(user_id, tweet_id)
        if like:
            await self.db_session.delete(like)
            await self.db_session.commit()
            return True
        return False

    async def get_like(self, user_id: int, tweet_id: int) -> Like | None:
        """Проверка стоит есть ли лайк"""
        result = await self.db_session.execute(
            select(Like)
            .filter(Like.user_id == user_id)
            .filter(Like.tweet_id == tweet_id)
        )
        return result.scalars().first()
