from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase

TEST_USER_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={
            'full_name': 'Ivan Ivanovich',
            'email': 'example23@gmail.com',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'full_name': 'Ivan Ivanovich',
            'email': 'example23@gmail.com',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={
            'full_name': 'Ivan Ivanov',
            'email': 'examplegmail.com',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Non-valid email',
    ),
]

TEST_USER_ROUTE_DELETE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_204_NO_CONTENT,
        expected_data={},
        description='Positive case - delete existing user',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/3d3e784f-646a-4ad4-544c-dca5dcea2a11',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent user',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/invalid-id',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Invalid user ID format',
    ),
]
