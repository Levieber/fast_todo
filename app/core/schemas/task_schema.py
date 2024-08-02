from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., title="Task title", min_length=3, max_length=50)
    description: str = Field(
        ..., title="Task description", min_length=3, max_length=150
    )
    status: Optional[bool] = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[bool] = False


class TaskDetail(BaseModel):
    id: UUID
    status: bool
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
