from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user, get_user_service
from app.models.user import User
from app.schemas.user import (
    SuccessResponseUserSchema,
    UserBaseSchema,
    UserCreateRequestSchema,
    UserProfileSchema,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/create",
    summary="Создать пользователя",
    response_model=UserBaseSchema,
)
async def create_user(
    user_data: UserCreateRequestSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    """
    Эндпоинт для создания пользователя
    """

    return await user_service.create_user_with_generated_key(user_data=user_data)


@router.get(
    "/me", summary="Получить информацию и себе", response_model=UserProfileSchema
)
async def read_user_me(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: User = Depends(get_current_user),
):
    """
    Эндпоинт для получения информации и себе
    """
    return await user_service.get_user_by_api_key(current_user.api_key)


@router.get(
    "/{user_id}",
    summary="Получить информацию и произвольном профиле",
    response_model=UserProfileSchema,
)
async def read_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
):
    """
    Эндпоинт для получения информации о любом пользователе по его id
    """
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
    """
    Эндпоинт для подписки на другого пользователя
    """
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
    """
    Эндпоинт для отдписки на другого пользователя
    """
    return await user_service.unfollow_user(current_user.id, user_id)
