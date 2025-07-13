from datetime import date

from pydantic import BaseModel

from app.models.todo_item import TodoStatus


class TodoItemBase(BaseModel):
    name: str
    deadline: date | None = None


class TodoItemCreate(TodoItemBase):
    pass


class TodoItemUpdate(TodoItemBase):
    status: TodoStatus | None = None


class TodoItem(TodoItemBase):
    id: int
    status: TodoStatus
    todo_list_id: int

    class Config:
        from_attributes = True
