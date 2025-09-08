from typing import List

from pydantic import BaseModel, ConfigDict, Field


class UserBaseSchema(BaseModel):
    name: str
    api_key: str


class SuccessResponseUserSchema(BaseModel):
    result: bool = Field(True, description="Флаг успешного выполнения операции")


class UserCreate(UserBaseSchema):
    pass


class UserBaseSchema(BaseModel):
    name: str = Field(..., examples=["John"])
    api_key: str = Field(..., examples=["api-key"])

    model_config = ConfigDict(from_attributes=True)


class UserCreateRequestSchema(BaseModel):
    name: str = Field(..., examples=["Vova"])

    model_config = ConfigDict(
        from_attributes=True,
    )



class UserShortSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserProfileSchema(BaseModel):
    id: int
    name: str
    followers: List[UserShortSchema] = []
    following: List[UserShortSchema] = []

    model_config = ConfigDict(from_attributes=True)
