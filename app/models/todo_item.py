import enum

from sqlalchemy import Column, Date
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class TodoStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoItem(Base):
    __tablename__ = "todo_items"  # type: ignore

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    status = Column(SQLAlchemyEnum(TodoStatus),
                    default=TodoStatus.PENDING, nullable=False)
    deadline = Column(Date)
    todo_list_id = Column(Integer, ForeignKey("todo_lists.id"))

    todo_list = relationship("TodoList", back_populates="items")
