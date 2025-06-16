from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.schemas.user import UserDB

if TYPE_CHECKING:
    from src.models.task import Task


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(UTC))

    authored_tasks: Mapped['Task'] = relationship(back_populates='author', foreign_keys='Task.author_id')
    assigned_tasks: Mapped['Task'] = relationship(back_populates='assignee', foreign_keys='Task.assignee_id')
    watching_tasks: Mapped[list['Task']] = relationship(secondary='task_watchers', back_populates='watchers')
    executing_tasks: Mapped[list['Task']] = relationship(secondary='task_executors', back_populates='executors')

    def to_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
