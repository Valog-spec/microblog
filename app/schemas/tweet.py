from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.media import MediaBaseSchema
from app.schemas.user import UserShortSchema


class TweetBaseSchema(BaseModel):
    content: str
    tweet_media_ids: Optional[List[int]] = Field(
        default=None, examples=[None], description="Список ID медиафайлов для твита"
    )


class TweetCreateSchema(TweetBaseSchema):
    pass


class TweetSchema(TweetBaseSchema):
    id: int
    author: UserShortSchema
    likes: List[UserShortSchema] = []
    attachments: List[MediaBaseSchema] = []

    model_config = ConfigDict(
        from_attributes=True,
    )


class SuccessResponseTweetSchema(BaseModel):
    result: bool = Field(True, description="Флаг успешного выполнения операции")
    tweet_id: int | None = None


class TweetsGetFeedSchema(BaseModel):
    result: bool = Field(True, description="Флаг успешного выполнения")
    tweets: List[TweetSchema] = Field(..., description="Список твитов")
