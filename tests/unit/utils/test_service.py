from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserDB
from tests.fixtures import FakeBaseService, testing_cases
from tests.utils import (
    BaseTestCase,
    TestIdCase,
    compare_dicts_and_db_models,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from src.models import User


class TestBaseService:
    class _BaseService(FakeBaseService):
        _repo = 'user'

    def __get_service(self, session: AsyncSession) -> FakeBaseService:
        return self._BaseService(session)

    async def test_add_one_and_get_obj(
            self,
            transaction_session: AsyncSession,
            first_user: dict,
            get_users: Callable[..., Awaitable[Any]],
    ) -> None:
        service = self.__get_service(transaction_session)
        user = await service.add_one_and_get_obj(**first_user)
        assert user.id == first_user.get('id')

        users_in_db: Sequence[User] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS)
    async def test_get_by_filter_one_or_none(
            self,
            case: BaseTestCase,
            transaction_session: AsyncSession,
    ) -> None:
        service = self.__get_service(transaction_session)
        with case.expected_error:
            user_in_db: User | None = await service.get_by_filter_one_or_none(**case.data)
            result = None if not user_in_db else user_in_db.to_schema()
            assert result == case.expected_data

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS)
    async def test_update_one_by_id(
            self,
            case: BaseTestCase,
            transaction_session: AsyncSession,
    ) -> None:
        service = self.__get_service(transaction_session)
        with case.expected_error:
            updated_user: User | None = await service.update_one_by_id(case.data.pop('_id'), **case.data)
            assert updated_user.to_schema() == case.expected_data

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_BASE_SERVICE_DELETE_BY_IDS)
    async def test_delete_by_ids(
            self,
            case: TestIdCase,
            transaction_session: AsyncSession,
            get_users: Callable[..., Awaitable[Any]],
    ) -> None:
        service = self.__get_service(transaction_session)
        with case.expected_error:
            await service.delete_by_ids(*case.data)
            users_in_db: Sequence[User] = await get_users()
            assert compare_dicts_and_db_models(users_in_db, case.expected_data, UserDB)
