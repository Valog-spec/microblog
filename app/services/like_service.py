from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.like_repository import LikeRepository
from app.schemas.like import SuccessResponseLikeSchema


class LikeService:
    """Репозиторий для работы с лайками"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.like_repository = LikeRepository(db_session=db_session)

    async def create_like(
        self, user_id: int, tweet_id: int
    ) -> SuccessResponseLikeSchema:
        """Поставить лайк по id пользователя и твиту"""
        await self.like_repository.create_like(user_id=user_id, tweet_id=tweet_id)

        return SuccessResponseLikeSchema(result=True)

    async def delete_like(
        self, user_id: int, tweet_id: int
    ) -> SuccessResponseLikeSchema:
        """Убрать лайк по id пользователя и твиту"""

        result = await self.like_repository.delete_like(
            user_id=user_id, tweet_id=tweet_id
        )
        if not result:
            raise HTTPException(status_code=404, detail="Like not found")

        return SuccessResponseLikeSchema(result=True)
