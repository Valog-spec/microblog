from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_like_service
from app.models.user import User
from app.schemas.like import SuccessResponseLikeSchema
from app.services.like_service import LikeService

router = APIRouter(prefix="/api/likes", tags=["likes"])


@router.post(
    "/{tweet_id}/likes",
    summary="Поставить лайк на твит",
    response_model=SuccessResponseLikeSchema,
)
async def like_tweet(
    tweet_id: int,
    like_service: Annotated[LikeService, Depends(get_like_service)],
    current_user: User = Depends(get_current_user),
) -> SuccessResponseLikeSchema:
    """
    Эндпоинт для проставления лайка на твит
    """
    return await like_service.create_like(user_id=current_user.id, tweet_id=tweet_id)


@router.delete(
    "/{tweet_id}/likes",
    summary="Удалить лайк на твит",
    response_model=SuccessResponseLikeSchema,
)
async def unlike_tweet(
    tweet_id: int,
    like_service: Annotated[LikeService, Depends(get_like_service)],
    current_user: User = Depends(get_current_user),
) -> SuccessResponseLikeSchema:
    """
    Эндпоинт для удаления лайка на твит
    """
    return await like_service.delete_like(user_id=current_user.id, tweet_id=tweet_id)
