import os
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.core.dependencies import get_current_user, get_media_service
from app.models.user import User
from app.schemas.media import SuccessResponseMediaSchema
from app.services.media_service import MediaService

router = APIRouter(prefix="/api/media", tags=["media"])


MEDIA_DIR = "app/static/media"
os.makedirs(MEDIA_DIR, exist_ok=True)


@router.post(
    "", summary="Загрузить медиафайл к твиту", response_model=SuccessResponseMediaSchema
)
async def upload_media(
    file: Annotated[UploadFile, File(...)],
    tweet_service: Annotated[MediaService, Depends(get_media_service)],
    current_user: User = Depends(get_current_user),
) -> SuccessResponseMediaSchema:
    """Сохраняет медиафайл на сервере и создает запись в базе данных"""

    file_ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(MEDIA_DIR, file_name)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    relative_path = f"/app/static/media/{file_name}"

    return await tweet_service.create_media(relative_path, current_user.id)
