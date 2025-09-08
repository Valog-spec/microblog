from typing import Optional

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.media import Media


class MediaRepository:
    """Репозиторий для работы с медиа файлами"""

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_media(self, file_path: str, user_id: int) -> Media:
        """Загруить медиа файл для твита по его id"""
        db_media = Media(url=file_path, uploaded_by=user_id)
        self.db_session.add(db_media)
        await self.db_session.commit()
        await self.db_session.refresh(db_media)
        return db_media


    async def get_user_media(self, media_id: int, user_id: int) -> Optional[Media]:
        result = await self.db_session.execute(
            select(Media).where(and_(Media.id == media_id, Media.uploaded_by == user_id))
        )
        return result.scalar_one_or_none()

    # async def attach_media_to_tweet(self, media_ids: list[int], tweet_id: int):
    #     for media_id in media_ids:
    #         media = await self.get_media(media_id)
    #         if media:
    #             media.tweet_id = tweet_id
    #     await self.db_session.commit()
    #
    # async def get_media(self, media_id: int):
    #     result = await self.db_session.execute(select(Media).filter(Media.id == media_id))
    #     return result.scalars().first()
