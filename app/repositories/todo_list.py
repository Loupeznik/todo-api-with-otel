from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.todo_list import TodoList
from app.schemas.todo_list import TodoListCreate, TodoListUpdate


class TodoListRepository:
    def get_todo_list(self, db: Session, todo_list_id: int) -> Optional[TodoList]:
        """
        Retrieve a to-do list by its ID.
        """
        return db.query(TodoList).filter(TodoList.id == todo_list_id).first()

    def get_todo_lists_by_owner(self, db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[TodoList]:
        """
        Retrieve all to-do lists for a specific owner, with pagination.
        """
        return db.query(TodoList).filter(TodoList.owner_id == owner_id).offset(skip).limit(limit).all()

    def create_todo_list(self, db: Session, *, obj_in: TodoListCreate, owner_id: int) -> TodoList:
        """
        Create a new to-do list for a given user.
        """
        db_obj = TodoList(**obj_in.model_dump(),
                          owner_id=owner_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_todo_list(
        self, db: Session, *, db_obj: TodoList, obj_in: TodoListUpdate
    ) -> TodoList:
        """
        Update a to-do list's details.
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_todo_list(self, db: Session, *, id: int) -> Optional[TodoList]:
        """
        Delete a to-do list from the database.
        """
        obj = db.query(TodoList).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


todo_list_repo = TodoListRepository()
