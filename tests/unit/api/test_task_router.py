from httpx import AsyncClient
from starlette import status

import pytest
from tests.fixtures import testing_cases
from tests.utils import AnyUUID, RequestTestCase, prepare_payload


class TestTaskRouter:

    @staticmethod
    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_CREATE_PARAMS)
    async def test_create(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.post(case.url, json=case.data, headers=case.headers)
            assert response.status_code == case.expected_status

            response_data = response.json()

            if case.expected_status in (status.HTTP_200_OK, status.HTTP_201_CREATED):
                assert response_data['status'] == case.expected_data['status']
                assert response_data['error'] == case.expected_data['error']
                assert AnyUUID() == response_data['payload']

            elif case.expected_status == status.HTTP_422_UNPROCESSABLE_ENTITY:
                assert 'detail' in response_data
                assert isinstance(response_data['detail'], list)

            else:
                assert response_data == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_GET_PARAMS)
    async def test_get(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.get(case.url, headers=case.headers)
            assert response.status_code == case.expected_status
            assert prepare_payload(response, ['id']) == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_DELETE_PARAMS)
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
