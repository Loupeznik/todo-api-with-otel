from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class TodoList(Base):
    __tablename__ = "todo_lists"  # type: ignore

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="todo_lists")
    items = relationship(
        "TodoItem", back_populates="todo_list", cascade="all, delete-orphan")
