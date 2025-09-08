from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    SuccessResponseUserSchema,
    UserBaseSchema,
    UserCreateRequestSchema,
    UserProfileSchema,
)


class UserService:
    """Сервис для работы с пользователем"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.user_repository = UserRepository(db_session=db_session)

    async def create_user_with_generated_key(
        self, user_data: UserCreateRequestSchema
    ) -> UserBaseSchema:
        """Создание пользователя"""
        user = await self.user_repository.create_user_with_generated_key(user_data)

        return UserBaseSchema.model_validate(user)

    async def get_user_by_api_key(self, api_key: str) -> UserProfileSchema:
        """Получение пользователя по ключу"""

        user = await self.user_repository.get_user_by_api_key(api_key)

        return UserProfileSchema.model_validate(user)

    async def get_user(self, user_id: int) -> UserProfileSchema:
        """Получение пользователя по id"""

        user = await self.user_repository.get_user(user_id=user_id)

        return UserProfileSchema.model_validate(user)

    async def follow_user(
        self, follower_id: int, followed_id: int
    ) -> SuccessResponseUserSchema:
        """Подписка на пользователя"""

        if follower_id == followed_id:
            raise HTTPException(status_code=400, detail="Cannot follow yourself")

        result = await self.user_repository.follow_user(follower_id, followed_id)
        if not result:
            raise HTTPException(status_code=400, detail="Already following this user")

        return SuccessResponseUserSchema(result=True)

    async def unfollow_user(
        self, follower_id: int, followed_id: int
    ) -> SuccessResponseUserSchema:
        """Отписка от пользователя"""
        if follower_id == followed_id:
            raise HTTPException(status_code=400, detail="Cannot unfollow yourself")
        result = await self.user_repository.unfollow_user(follower_id, followed_id)

        if not result:
            raise HTTPException(status_code=400, detail="Not following this user")

        return SuccessResponseUserSchema(result=True)
