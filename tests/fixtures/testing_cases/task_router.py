from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import AnyUUID, RequestTestCase

TEST_TASK_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/',
        headers={},
        data={
            'title': 'test1',
            'status': 'todo',
            'author_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'status': 200,
            'error': False,
            'payload': AnyUUID(),
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/',
        headers={},
        data={
            'title': 'test1',
            'status': 'todo',
            'author_id': '00000000-0000-0000-0000-000000000000',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Non-existent user',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
]

TEST_TASK_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/b04e55bd-8431-4edd-8eb4-632099c0ea65',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'title': 'test1',
            'status': 'todo',
            'author_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/1',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid user id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/b04e55bd-8431-4edd-8eb4-632099c0ea60',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent user',
    ),
]

TEST_TASK_ROUTE_DELETE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/b04e55bd-8431-4edd-8eb4-632099c0ea65',
        headers={},
        expected_status=HTTP_204_NO_CONTENT,
        expected_data=None,
        description='Positive case - delete existing task',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/b04e55bd-8431-4edd-8eb4-632078c0ea63',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent task',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/task/invalid-id',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Invalid task ID format',
    ),
]
