from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.media_repository import MediaRepository
from app.repositories.tweet_repository import TweetRepository
from app.schemas.media import MediaBaseSchema
from app.schemas.tweet import (SuccessResponseTweetSchema, TweetSchema,
                               TweetsGetFeedSchema)
from app.schemas.user import UserShortSchema


class TweetService:
    """Сервис для работы с твитами"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.tweet_repository = TweetRepository(db_session=db_session)
        self.media_repository = MediaRepository(db_session=db_session)

    async def create_tweet(
        self, content: str, author_id: int, media_ids: List[int] = None
    ) -> SuccessResponseTweetSchema:
        """Создать твит"""
        media_ids = media_ids or []

        if media_ids:
            for media_id in media_ids:
                media = await self.media_repository.get_user_media(media_id, author_id)
                if not media:
                    raise Exception(
                        "Ничего не найдено, либо не принадлежит пользователю"
                    )

        tweet = await self.tweet_repository.create_tweet(content, author_id, media_ids)

        return SuccessResponseTweetSchema(result=True, tweet_id=tweet.id)

    async def delete_tweet(
        self, tweet_id: int, author_id: int
    ) -> SuccessResponseTweetSchema:
        """Удалить твит"""
        result = await self.tweet_repository.delete_tweet(
            tweet_id=tweet_id, author_id=author_id
        )
        if not result:
            raise HTTPException(
                status_code=404, detail="Tweet not found or not authorized"
            )

        return SuccessResponseTweetSchema(result=True)

    async def get_tweets_feed(
        self, user_id: int, limit: int = 100
    ) -> TweetsGetFeedSchema:
        """Полуить ленту с твитами"""
        tweets = await self.tweet_repository.get_tweets_feed(
            user_id=user_id, limit=limit
        )

        return TweetsGetFeedSchema(
            result=True,
            tweets=[
                TweetSchema(
                    id=tweet.id,
                    content=tweet.content,
                    attachments=[
                        MediaBaseSchema(url=media.url) for media in tweet.media
                    ],
                    author=UserShortSchema(id=tweet.author.id, name=tweet.author.name),
                    likes=[
                        UserShortSchema(id=like.user.id, name=like.user.name)
                        for like in tweet.likes
                    ],
                )
                for tweet in tweets
            ],
        )
