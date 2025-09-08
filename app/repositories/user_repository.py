import uuid

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.user import User, followers
from app.schemas.user import UserCreateRequestSchema


class UserRepository:
    """Репозиторий для работы с пользователем"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def generate_api_key(self) -> str:
        """Получение уникального идентификатора"""
        return str(uuid.uuid4())

    async def create_user_with_generated_key(
        self, user_data: UserCreateRequestSchema
    ) -> User:
        """Создание пользователя"""
        api_key = await self.generate_api_key()
        db_user = User(name=user_data.name, api_key=api_key)
        self.db_session.add(db_user)
        await self.db_session.commit()
        await self.db_session.refresh(db_user)
        return db_user

    async def get_user_by_api_key(self, api_key: str) -> User:
        """Получение пользователя по его api_key"""
        result = await self.db_session.execute(
            select(User).filter(User.api_key == api_key)
        )
        user = result.scalars().first()
        await self.db_session.refresh(user, ["following"])
        await self.db_session.refresh(user, ["followers"])
        return user

    async def get_user(self, user_id: int) -> User:
        """Получение пользователя по его id"""
        result = await self.db_session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.db_session.refresh(user, ["following"])
        await self.db_session.refresh(user, ["followers"])
        return user

    async def follow_user(self, follower_id: int, followed_id: int) -> bool:
        """Подписка на другого пользователя"""
        follower = await self.get_user(follower_id)
        followed = await self.get_user(followed_id)
        if not follower or not followed:
            return False

        query = (
            select(User)
            .where(User.id == follower_id)
            .options(selectinload(User.following))
        )
        follower = await self.db_session.execute(query)
        follower = follower.scalar_one()

        exists_query = (
            select(followers)
            .where(followers.c.follower_id == follower_id)
            .where(followers.c.followed_id == followed_id)
        )
        existing_follow = await self.db_session.execute(exists_query)
        if existing_follow.scalar():
            return False

        insert_stmt = followers.insert().values(
            follower_id=follower_id, followed_id=followed_id
        )
        await self.db_session.execute(insert_stmt)
        await self.db_session.commit()

        return True

    async def unfollow_user(self, follower_id: int, followed_id: int) -> bool:
        """Отписка от другого пользователя"""

        delete_stmt = (
            followers.delete()
            .where(followers.c.follower_id == follower_id)
            .where(followers.c.followed_id == followed_id)
        )
        result = await self.db_session.execute(delete_stmt)
        await self.db_session.commit()

        return result.rowcount > 0
