from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_tweet_service
from app.models.user import User
from app.schemas.tweet import (
    SuccessResponseTweetSchema,
    TweetCreateSchema,
    TweetsGetFeedSchema,
)
from app.services.tweet_service import TweetService

router = APIRouter(prefix="/api/tweets", tags=["tweets"])


@router.post("", summary="Создать твит", response_model=SuccessResponseTweetSchema)
async def create_new_tweet(
    tweet_data: TweetCreateSchema,
    tweet_service: Annotated[TweetService, Depends(get_tweet_service)],
    current_user: User = Depends(get_current_user),
):
    """
    Эндпоинт для создания твита
    """
    return await tweet_service.create_tweet(tweet_data.content, current_user.id, tweet_data.tweet_media_ids)

    # db_tweet = await create_tweet(db, tweet_data, current_user.id)
    #
    # if tweet_data.tweet_media_ids:
    #     await attach_media_to_tweet(db, tweet_data.tweet_media_ids, db_tweet.id)
    #
    # return {"result": True, "tweet_id": db_tweet.id}


@router.delete(
    "/{tweet_id}", summary="Удалить твит", response_model=SuccessResponseTweetSchema
)
async def delete_user_tweet(
    tweet_id: int,
    tweet_service: Annotated[TweetService, Depends(get_tweet_service)],
    current_user: User = Depends(get_current_user),
) -> SuccessResponseTweetSchema:
    """
    Эндпоинт для удаления твита
    """
    return await tweet_service.delete_tweet(
        tweet_id=tweet_id, author_id=current_user.id
    )


@router.get("", summary="Получить ленту твитов", response_model=TweetsGetFeedSchema)
async def get_user_feed(
    tweet_service: Annotated[TweetService, Depends(get_tweet_service)],
    current_user: User = Depends(get_current_user),
) -> SuccessResponseTweetSchema:
    """
    Эндпоинт для получения всей ленты твитов
    """
    return await tweet_service.get_tweets_feed(current_user.id)
