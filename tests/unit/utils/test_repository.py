from collections.abc import Awaitable, Callable

from typing import TYPE_CHECKING, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.user import UserDB
from src.utils.repository import SqlAlchemyRepository

import pytest
from tests.fixtures import testing_cases
from tests.utils import BaseTestCase, TestIdCase, compare_dicts_and_db_models


if TYPE_CHECKING:
    from collections.abc import Sequence


class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        _model = User

    def __get_sql_rep(self, session: AsyncSession) -> SqlAlchemyRepository:
        return self._SqlAlchemyRepository(session)

    async def test_add_one_and_get_obj(
            self,
            transaction_session: AsyncSession,
            first_user: dict,
            get_users: Callable[..., Awaitable[Any]],
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        user = await sql_rep.add_one_and_get_obj(**first_user)
        assert user.id == first_user.get('id')
        await transaction_session.flush()

        users_in_db: Sequence[User] = await get_users()
        assert compare_dicts_and_db_models(users_in_db, [first_user], UserDB)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE_PARAMS)
    async def test_get_by_filter_one_or_none(
            self,
            case: BaseTestCase,
            transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            user_in_db: User | None = await sql_rep.get_by_filter_one_or_none(**case.data)
            result = None if not user_in_db else user_in_db.to_schema()
            assert result == case.expected_data

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID_PARAMS)
    async def test_update_one_by_id(
            self,
            case: BaseTestCase,
            transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            updated_user: User | None = await sql_rep.update_one_by_id(case.data.pop('_id'), **case.data)
            assert updated_user.to_schema() == case.expected_data

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_IDS)
    async def test_delete_by_ids(
            self,
            case: TestIdCase,
            transaction_session: AsyncSession,
            get_users: Callable[..., Awaitable[Any]],
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            await sql_rep.delete_by_ids(*case.data)
            await transaction_session.flush()
            users_in_db: Sequence[User] = await get_users()
            assert compare_dicts_and_db_models(users_in_db, case.expected_data, UserDB)
