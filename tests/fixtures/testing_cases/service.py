from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import MultipleResultsFound

from src.schemas.user import UserDB
from tests.fixtures.db_mocks import USERS
from tests.utils import BaseTestCase, TestIdCase

TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'full_name': 'Elon Musk'},
        expected_data=UserDB(
            id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
            full_name='Elon Musk',
            email='example2@gmail.com'),
    ),
    BaseTestCase(
        data={'full_name': 'Liza Ivanova'},
        expected_data=None,
    ),
    BaseTestCase(
        data={'full_name': 'Ivan Ivanov'},
        expected_data=None,
        expected_error=pytest.raises(MultipleResultsFound),
    ),
]

TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS: list[BaseTestCase] = [
    BaseTestCase(data={'full_name': 'Elon Musk'}, expected_data=[USERS[1]]),
    BaseTestCase(data={'full_name': 'Liza Ivanova'}, expected_data=[]),
    BaseTestCase(data={'full_name': 'Ivan Ivanov'}, expected_data=[USERS[0], USERS[2]]),
]

TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'_id': USERS[0]['id'], 'full_name': 'Liza Ivanova'},
        expected_data=UserDB(
            id=UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
            full_name='Liza Ivanova',
            email='example@gmail.com'),
    ),
]

TEST_BASE_SERVICE_DELETE_BY_IDS: list[TestIdCase] = [
    TestIdCase(data=[USERS[0]['id']], expected_data=USERS[1:]),
    TestIdCase(data=[uuid4()], expected_data=USERS),
    TestIdCase(data=[], expected_data=USERS),
]
