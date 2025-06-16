from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base

if TYPE_CHECKING:
    from src.models.task import Task
    from src.models.task_watcher import TaskWatcher
    from src.models.task_executor import TaskExecutor


class TaskExecutor(Base):
    __tablename__ = 'task_executors'

    task_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey('tasks.id'), primary_key=True)
    user_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
