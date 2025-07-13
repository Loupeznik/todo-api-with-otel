from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import db as database
from app import models, schemas
from app.api import deps
from app.repositories.todo_list import todo_list_repo

router = APIRouter()


@router.post("/", response_model=schemas.TodoList)
def create_todo_list(
    *,
    db: Session = Depends(deps.get_db),
    todo_list_in: schemas.TodoListCreate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Create new todo list.
    """
    return todo_list_repo.create_todo_list(
        db=db, obj_in=todo_list_in, owner_id=current_user.id  # type: ignore
    )


@router.get("/", response_model=List[schemas.TodoList])
def read_todo_lists(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Retrieve user's todo lists.
    """
    return todo_list_repo.get_todo_lists_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit  # type: ignore
    )


@router.get("/{id}", response_model=schemas.TodoList)
def read_todo_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Get todo list by ID.
    """
    todo_list = todo_list_repo.get_todo_list(db=db, todo_list_id=id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    if todo_list.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return todo_list


@router.put("/{id}", response_model=schemas.TodoList)
def update_todo_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    todo_list_in: schemas.TodoListUpdate,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Update a todo list.
    """
    todo_list = todo_list_repo.get_todo_list(db=db, todo_list_id=id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    if todo_list.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=403, detail="Not enough permissions")
    todo_list = todo_list_repo.update_todo_list(
        db=db, db_obj=todo_list, obj_in=todo_list_in)
    return todo_list


@router.delete("/{id}", response_model=schemas.TodoList)
def delete_todo_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
):
    """
    Delete a todo list.
    """
    todo_list = todo_list_repo.get_todo_list(db=db, todo_list_id=id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")
    if todo_list.owner_id != current_user.id:  # type: ignore
        raise HTTPException(status_code=403, detail="Not enough permissions")
    todo_list = todo_list_repo.remove_todo_list(db=db, id=id)
    return todo_list
