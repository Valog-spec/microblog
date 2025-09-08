from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_user_service
from app.logger.logger_helper import get_logger
from app.models.user import User
from app.schemas.user import (
    SuccessResponseUserSchema,
    UserBaseSchema,
    UserCreateRequestSchema,
    UserProfileSchema,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])

logger = get_logger("logger.user_endpoint")


@router.post(
    "/create",
    summary="Создать пользователя",
    response_model=UserBaseSchema,
)
async def create_user(
    user_data: UserCreateRequestSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Создает нового пользователя с автоматической генерацией API ключа"""
    logger.info("Создание пользователя: name=%s", user_data.name)

    return await user_service.create_user_with_generated_key(user_data=user_data)


@router.get(
    "/me", summary="Получить информацию и себе", response_model=UserProfileSchema
)
async def read_user_me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: User = Depends(get_current_user),
):
    """Возвращает профиль текущего аутентифицированного пользователя"""
    return await user_service.get_user_by_api_key(current_user.api_key)


@router.get(
    "/{user_id}",
    summary="Получить информацию и произвольном профиле",
    response_model=UserProfileSchema,
)
async def read_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
):
    """Возвращает профиль пользователя по указанному ID"""
    return await user_service.get_user(user_id)


@router.post(
    "/{user_id}/follow",
    summary="Подписаться другого пользователя",
    response_model=SuccessResponseUserSchema,
)
async def follow_user_endpoint(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: User = Depends(get_current_user),
):
    """Добавляет подписку текущего пользователя на указанного пользователя"""
    return await user_service.follow_user(current_user.id, user_id)


@router.delete(
    "/{user_id}/follow",
    summary="Отписатья от пользователя",
    response_model=SuccessResponseUserSchema,
)
async def unfollow_user_endpoint(
    user_id: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: User = Depends(get_current_user),
):
    """Удаляет подписку текущего пользователя на указанного пользователя"""
    return await user_service.unfollow_user(current_user.id, user_id)
