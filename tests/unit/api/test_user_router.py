from httpx import AsyncClient
from starlette import status

import pytest
from tests.fixtures import testing_cases
from tests.utils import RequestTestCase, prepare_payload


class TestUserRouter:

    @staticmethod
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_USER_ROUTE_CREATE_PARAMS)
    async def test_create(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.post(case.url, json=case.data, headers=case.headers)
            assert response.status_code == case.expected_status
            assert prepare_payload(response, ['id']) == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_USER_ROUTE_DELETE_PARAMS)
    async def test_delete(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.delete(case.url, headers=case.headers)

            if case.expected_status == status.HTTP_204_NO_CONTENT:
                assert not response.content
            elif case.expected_data is not None:
                assert prepare_payload(response) == case.expected_data
