from pydantic import BaseModel, ConfigDict, Field


class LikeBaseSchema(BaseModel):
    pass


class SuccessResponseLikeSchema(BaseModel):
    result: bool = Field(True, description="Флаг успешного выполнения операции")
