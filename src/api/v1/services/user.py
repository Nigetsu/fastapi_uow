from typing import TYPE_CHECKING

from pydantic import UUID4

from src.schemas.user import UserCreateRequest, UserDB
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from src.models import User


class UserService(BaseService):
    _repo: str = 'user'

    @transaction_mode
    async def create_user(self, user: UserCreateRequest) -> UserDB:
        created_user: User = await self.uow.user.add_one_and_get_obj(**user.model_dump())
        return created_user.to_schema()

    @transaction_mode
    async def delete_user(self, user_id: UUID4) -> None:
        await self.uow.user.delete_by_ids(user_id)
