from typing import TYPE_CHECKING

from pydantic import UUID4

from src.schemas.task import TaskCreateRequest, TaskDB, TaskFilters, TaskUpdateRequest
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from collections.abc import Sequence

    from src.models import Task


class TaskService(BaseService):
    _repo: str = 'task'

    @transaction_mode
    async def create_task(self, task: TaskCreateRequest) -> TaskDB:
        create_task: Task = await self.uow.task.add_one_and_get_obj(**task.model_dump())
        return create_task.to_schema()

    @transaction_mode
    async def get_task_by_id(self, task_id: UUID4) -> TaskDB:
        task: Task | None = await self.uow.task.get_by_filter_one_or_none(id=task_id)
        self.check_existence(obj=task, details='Task not found')
        return task.to_schema()

    @transaction_mode
    async def update_task(self, task_id: UUID4, task: TaskUpdateRequest) -> TaskDB:
        task: Task | None = await self.uow.task.update_one_by_id(obj_id=task_id, **task.model_dump())
        self.check_existence(obj=task, details='Task not found')
        return task.to_schema()

    @transaction_mode
    async def delete_task(self, task_id: UUID4) -> None:
        await self.uow.task.delete_by_ids(task_id)

    @transaction_mode
    async def get_tasks_by_filters(self, filters: TaskFilters) -> list[TaskDB]:
        tasks: Sequence[Task] = await self.uow.task.get_tasks_by_filters(filters)
        return [task.to_schema() for task in tasks]
