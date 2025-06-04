from pydantic import UUID4, BaseModel, Field
from src.schemas.response import BaseCreateResponse


class UserID(BaseModel):
    id: UUID4


class UserCreateRequest(BaseModel):
    full_name: str = Field(max_length=100)
    email: str = Field(max_length=120)


class UserDB(UserID, UserCreateRequest):
    pass


class UserCreateResponse(BaseCreateResponse):
    payload: UserDB
