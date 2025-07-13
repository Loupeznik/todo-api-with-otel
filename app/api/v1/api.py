from fastapi import APIRouter

from app.api.v1.endpoints import health, todo_items, todo_lists, users

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(todo_lists.router, prefix="/lists", tags=["todo-lists"])
api_router.include_router(todo_items.router, prefix="/items", tags=["todo-items"])
