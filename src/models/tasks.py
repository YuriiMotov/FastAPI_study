from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base
from schemas.tasks import TaskSchema, TaskHistorySchema


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    assignee_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def to_read_model(self) -> TaskSchema:
        return TaskSchema(
            id=self.id, 
            title=self.title,
            author_id=self.author_id,
            assignee_id=self.assignee_id
        )


class TaskHistory(Base):
    __tablename__ = "task_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    previous_assignee_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    new_assignee_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def to_read_model(self) -> TaskHistorySchema:
        return TaskHistorySchema(
            id=self.id,
            task_id=self.task_id,
            previous_assignee_id=self.previous_assignee_id,
            new_assignee_id=self.new_assignee_id
        )