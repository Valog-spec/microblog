from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.media_repository import MediaRepository
from app.schemas.media import SuccessResponseMediaSchema


class MediaService:
    """Сервис для работы с медиа файлами"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.media_repository = MediaRepository(db_session=db_session)

    async def create_media(
        self, file_path: str, user_id: int = None
    ) -> SuccessResponseMediaSchema:
        """Добавить медиа файл в твит пользователя"""
        media = await self.media_repository.create_media(
            file_path=file_path, user_id=user_id
        )

        return SuccessResponseMediaSchema(result=True, media_id=media.id)
