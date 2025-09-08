from typing import Any, Coroutine, Sequence, List

from sqlalchemy import Row, RowMapping, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.media import Media
from app.models.tweet import Tweet
from app.schemas.tweet import TweetCreateSchema


class TweetRepository:
    """Репоизторий для работы с твитами"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_tweet(self, content: str, author_id: int, media_ids: List[int] = None) -> Tweet:
        """Создать твит"""
        db_tweet = Tweet(content=content, author_id=author_id)
        self.db_session.add(db_tweet)

        await self.db_session.flush()

        if media_ids:
            await self.db_session.execute(
                update(Media)
                .where(Media.id.in_(media_ids))
                .where(Media.uploaded_by == author_id)
                .values(tweet_id=db_tweet.id)
            )

        await self.db_session.commit()
        await self.db_session.refresh(db_tweet)
        return db_tweet

    async def get_tweet(self, tweet_id: int) -> Tweet:
        """Получить твит по его  id"""
        result = await self.db_session.execute(
            select(Tweet).filter(Tweet.id == tweet_id)
        )
        return result.scalars().first()

    async def delete_tweet(self, tweet_id: int, author_id: int) -> bool:
        """Удалить твит пользователя"""
        tweet = await self.get_tweet(tweet_id)
        if tweet and tweet.author_id == author_id:
            await self.db_session.delete(tweet)
            await self.db_session.commit()
            return True
        return False

    async def get_tweets_feed(self, user_id: int, limit: int = 100) -> Sequence[Tweet]:
        """Получение всей ленты твитов пользователя"""
        stmt = (
            select(Tweet)
            .where(Tweet.author_id == user_id)
            .limit(limit)
            .options(
                selectinload(Tweet.media),
                selectinload(Tweet.likes),
                selectinload(Tweet.author),
            )
        )
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
