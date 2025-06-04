from collections.abc import Sequence

from sqlalchemy import Result, select

from src.models import Task
from src.schemas.task import TaskFilters
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository[Task]):
    _model = Task

    async def get_tasks_by_filters(self, filters: TaskFilters) -> Sequence[Task]:
        query = select(self._model)

        if filters.author_id:
            query = query.where(self._model.author_id.in_(filters.author_id))

        if filters.status:
            query = query.where(self._model.status.in_(filters.status))

        if filters.assignee_id:
            query = query.where(self._model.status.in_(filters.assignee_id))

        res: Result = await self._session.execute(query)
        return res.scalars().all()
