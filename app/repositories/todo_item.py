from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.todo_item import TodoItem
from app.schemas.todo_item import TodoItemCreate, TodoItemUpdate


class TodoItemRepository:
    def get_todo_item(self, db: Session, todo_item_id: int) -> Optional[TodoItem]:
        """
        Retrieve a single to-do item by its ID.
        """
        return db.query(TodoItem).filter(TodoItem.id == todo_item_id).first()

    def get_todo_items_by_list(self, db: Session, todo_list_id: int, skip: int = 0, limit: int = 100) -> List[TodoItem]:
        """
        Retrieve all to-do items within a specific to-do list, with pagination.
        """
        return db.query(TodoItem).filter(TodoItem.todo_list_id == todo_list_id).offset(skip).limit(limit).all()

    def create_todo_item(self, db: Session, *, obj_in: TodoItemCreate, todo_list_id: int) -> TodoItem:
        """
        Create a new to-do item within a specific to-do list.
        """
        db_obj = TodoItem(**obj_in.model_dump(),
                          todo_list_id=todo_list_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_todo_item(self,
                         db: Session, *, db_obj: TodoItem, obj_in: TodoItemUpdate
                         ) -> TodoItem:
        """
        Update a to-do item's details.
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_todo_item(self, db: Session, *, id: int) -> Optional[TodoItem]:
        """
        Delete a to-do item from the database.
        """
        obj = db.query(TodoItem).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


todo_item_repo = TodoItemRepository()
