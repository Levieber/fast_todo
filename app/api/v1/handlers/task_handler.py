from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from api.dependencies.user_deps import get_current_user
from core.schemas.task_schema import TaskCreate, TaskDetail, TaskUpdate
from core.models.user_model import User
from core.models.task_model import Task
from core.services.task_service import TaskService


task_router = APIRouter()


@task_router.get("/", summary="List all tasks", response_model=List[TaskDetail])
async def index_tasks(user: User = Depends(get_current_user)) -> List[Task]:
    return await TaskService.list(user)


@task_router.post("/", summary="Create a task", response_model=TaskDetail)
async def create_task(data: TaskCreate, user: User = Depends(get_current_user)) -> Task:
    return await TaskService.create(user, data)


@task_router.get("/{id}", summary="Get a task by id", response_model=Task)
async def show_task(id: UUID, user: User = Depends(get_current_user)) -> Task:
    task = await TaskService.find(user, id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@task_router.put("/{id}", summary="Update a task", response_model=TaskDetail)
async def update_task(
    id: UUID, data: TaskUpdate, user: User = Depends(get_current_user)
):
    task = await TaskService.update(user, id, data)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


@task_router.delete(
    "/{id}", summary="Delete a task", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(id: UUID, user: User = Depends(get_current_user)):
    task = await TaskService.delete(user, id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
