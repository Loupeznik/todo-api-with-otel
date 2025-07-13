from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.repositories.todo_item import todo_item_repo
from app.repositories.todo_list import todo_list_repo

router = APIRouter()


@router.post("/", response_model=schemas.TodoItem)
def create_todo_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.TodoItemCreate,
    todo_list_id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create a new todo item inside a specific todo list.
    """
    todo_list = todo_list_repo.get_todo_list(db, todo_list_id=todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="Todo list not found")
    if todo_list.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return todo_item_repo.create_todo_item(db=db, obj_in=item_in, todo_list_id=todo_list_id)


@router.put("/{id}", response_model=schemas.TodoItem)
def update_todo_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.TodoItemUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a todo item.
    """
    db_item = todo_item_repo.get_todo_item(db=db, todo_item_id=id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_list = todo_list_repo.get_todo_list(
        db=db, todo_list_id=db_item.todo_list_id)  # type: ignore
    if todo_list.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = todo_item_repo.update_todo_item(
        db=db, db_obj=db_item, obj_in=item_in)
    return item


@router.delete("/{id}", response_model=schemas.TodoItem)
def delete_todo_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Delete a todo item.
    """
    db_item = todo_item_repo.get_todo_item(db=db, todo_item_id=id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    todo_list = todo_list_repo.get_todo_list(
        db=db, todo_list_id=db_item.todo_list_id)  # type: ignore
    if todo_list.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=403, detail="Not enough permissions")
    item = todo_item_repo.remove_todo_item(db=db, id=id)
    return item
