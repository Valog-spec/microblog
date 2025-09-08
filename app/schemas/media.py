from pydantic import BaseModel, ConfigDict, Field


class MediaBaseSchema(BaseModel):
    url: str


class MediaSchema(MediaBaseSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class SuccessResponseMediaSchema(BaseModel):
    result: bool = Field(True, description="Флаг успешного выполнения операции")
    media_id: int | None = None
