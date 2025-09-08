from fastapi import APIRouter

from app.endpoints import likes, media, tweets, users

routers = APIRouter()

routers.include_router(likes.router)
routers.include_router(media.router)
routers.include_router(tweets.router)
routers.include_router(users.router)
