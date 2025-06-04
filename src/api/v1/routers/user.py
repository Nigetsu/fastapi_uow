from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.api.v1.services.user import UserService
from src.schemas.user import (
    UserCreateRequest,
    UserCreateResponse,
    UserDB,
)

router = APIRouter(prefix='/user')


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
)
async def create_user(
        user: UserCreateRequest,
        service: UserService = Depends(UserService),
) -> UserCreateResponse:
    created_user: UserDB = await service.create_user(user)
    return UserCreateResponse(payload=created_user)


@router.delete(
    path='/{user_id}',
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: UUID4,
        service: UserService = Depends(),
) -> None:
    await service.delete_user(user_id)
