from typing import List

from pydantic import BaseModel

from .todo_item import TodoItem


class TodoListBase(BaseModel):
    name: str


class TodoListCreate(TodoListBase):
    pass


class TodoListUpdate(TodoListBase):
    pass


class TodoList(TodoListBase):
    id: int
    owner_id: int
    items: List[TodoItem] = []

    class Config:
        from_attributes = True
