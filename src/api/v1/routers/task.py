from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)

from src.api.v1.services import TaskService
from src.schemas.task import (
    TaskCreateRequest,
    TaskResponse,
    TaskDB,
    TasksListResponse,
    TaskFilters,
    TaskUpdateRequest,
    TaskCreateResponse,
)

router = APIRouter(prefix="/tasks")


@router.post(
    path="/",
    status_code=HTTP_201_CREATED,
)
async def create_task(
        task: TaskCreateRequest,
        service: TaskService = Depends(TaskService)
) -> TaskCreateResponse:
    created_task: TaskDB | None = await service.create_task(task)
    return TaskCreateResponse(payload=created_task)


@router.get(
    path="/filters/",
    status_code=HTTP_200_OK,
)
async def get_tasks_by_filters(
        filters: TaskFilters = Depends(),
        service: TaskService = Depends(),
) -> TasksListResponse:
    tasks = await service.get_tasks_by_filters(filters)
    return TasksListResponse(payload=tasks)


@router.get(
    "/{task_id}",
    status_code=HTTP_200_OK
)
async def get_task_by_id(
        task_id: UUID4,
        service: TaskService = Depends()
) -> TaskResponse:
    task: TaskDB | None = await service.get_task_by_id(task_id)
    return TaskResponse(payload=task)


@router.patch(
    path="/{user_id}",
    status_code=HTTP_200_OK,
)
async def update_user(
        task_id: UUID4,
        task: TaskUpdateRequest,
        service: TaskService = Depends(),
) -> TaskResponse:
    updated_task: TaskDB = await service.update_task(task_id, task)
    return TaskResponse(payload=updated_task)


@router.delete(
    path="/{user_id}",
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_task(
        task_id: UUID4,
        service: TaskService = Depends(),
) -> None:
    await service.delete_task(task_id)
