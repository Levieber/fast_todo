from typing import List, Literal, Optional
from uuid import UUID
from core.models.user_model import User
from core.models.task_model import Task
from core.schemas.task_schema import TaskCreate, TaskUpdate


class TaskService:
    @staticmethod
    async def list(user: User) -> List[Task]:
        tasks = await Task.find(
            Task.owner.id == user.id,  # type: ignore
            fetch_links=True,
        ).to_list()
        return tasks

    @staticmethod
    async def create(user: User, data: TaskCreate) -> Task:
        task = Task(**data.model_dump(), owner=user)  # type: ignore
        return await task.insert()

    @staticmethod
    async def find(user: User, id: UUID) -> Optional[Task]:
        task = await Task.find_one(Task.id == id, Task.owner.id == user.id)  # type: ignore
        return task

    @staticmethod
    async def update(user: User, id: UUID, data: TaskUpdate) -> Optional[Task]:
        task = await TaskService.find(user, id)

        if task is None:
            return None

        await task.update({"$set": data.model_dump(exclude_unset=True)})

        await task.save()

        return task

    @staticmethod
    async def delete(user: User, id: UUID) -> Optional[Literal[True]]:
        task = await TaskService.find(user, id)

        if task is None:
            return None

        await task.delete()

        return True
