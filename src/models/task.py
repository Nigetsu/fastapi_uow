from datetime import datetime, date, timezone
from enum import Enum
from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import (
    String, Text, ForeignKey, UUID,
    Enum as SQLAlchemyEnum,
    DateTime, Date, CheckConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.schemas.task import TaskDB

if TYPE_CHECKING:
    from src.models.user import User


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[TaskStatus] = mapped_column(SQLAlchemyEnum(TaskStatus), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    author_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    assignee_id: Mapped[Optional[uuid4]] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"))
    column_id: Mapped[Optional[uuid4]] = mapped_column(UUID(as_uuid=True), ForeignKey("columns.id"))
    sprint_id: Mapped[Optional[uuid4]] = mapped_column(UUID(as_uuid=True), ForeignKey("sprints.id"))
    board_id: Mapped[Optional[uuid4]] = mapped_column(UUID(as_uuid=True), ForeignKey("boards.id"))
    group_id: Mapped[Optional[uuid4]] = mapped_column(UUID(as_uuid=True), ForeignKey("groups.id"))

    author: Mapped["User"] = relationship(back_populates="authored_tasks", foreign_keys=[author_id])
    assignee: Mapped[Optional["User"]] = relationship(back_populates="assigned_tasks", foreign_keys=[assignee_id])
    column: Mapped[Optional["Column"]] = relationship(back_populates="tasks")
    sprint: Mapped[Optional["Sprint"]] = relationship(back_populates="tasks")
    board: Mapped[Optional["Board"]] = relationship(back_populates="tasks")
    group: Mapped[Optional["Group"]] = relationship(back_populates="tasks")
    watchers: Mapped[List["User"]] = relationship(secondary="task_watchers", back_populates="watching_tasks")
    executors: Mapped[List["User"]] = relationship(secondary="task_executors", back_populates="executing_tasks")

    def to_schema(self) -> TaskDB:
        return TaskDB(**self.__dict__)


class TaskWatcher(Base):
    __tablename__ = "task_watchers"

    task_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)


class TaskExecutor(Base):
    __tablename__ = "task_executors"

    task_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey("tasks.id"), primary_key=True)
    user_id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    columns: Mapped[List["Column"]] = relationship(back_populates="board", cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship(back_populates="board")


class Column(Base):
    __tablename__ = "columns"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)

    board: Mapped["Board"] = relationship(back_populates="columns")
    tasks: Mapped[List["Task"]] = relationship(back_populates="columns")


class Sprint(Base):
    __tablename__ = "sprints"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    start_date: Mapped[Optional[date]] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)

    __table_args__ = (
        CheckConstraint('end_date > start_date', name='check_sprint_dates'),
    )

    tasks: Mapped[List["Task"]] = relationship(back_populates="sprint")


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[uuid4] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    tasks: Mapped[List["Task"]] = relationship(back_populates="group")
