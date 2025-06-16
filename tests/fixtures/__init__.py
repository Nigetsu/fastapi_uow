__all__ = [
    'FakeBaseService',
    'FakeUnitOfWork',
    'TaskService',
    'UserService',
    'db_mocks',
    'testing_cases',
]

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.services import TaskService, UserService
from src.repositories import TaskRepository, UserRepository
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures import db_mocks, testing_cases


class FakeUnitOfWork(UnitOfWork):
    """Test class for overriding the standard UnitOfWork.
    Provides isolation using transactions at the level of a single TestCase.
    """

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session
        self.task = None
        self.user = None

    async def __aenter__(self) -> 'FakeUnitOfWork':
        self.task = TaskRepository(self._session)
        self.user = UserRepository(self._session)
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await self._session.flush()


class FakeBaseService(BaseService):
    """..."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)
