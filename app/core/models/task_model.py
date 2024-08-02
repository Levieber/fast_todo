from typing import Annotated
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed, Link, before_event, Replace, Insert
from pydantic import Field
from .user_model import User


class Task(Document):
    id: UUID = Field(default_factory=uuid4)
    status: bool = False
    title: Annotated[str, Indexed()]
    description: Annotated[str, Indexed()]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    owner: Link[User]

    def __repr__(self) -> str:
        return f"Task {self.title}"

    def __str__(self) -> str:
        return self.title

    def __hash__(self) -> int:
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Task):
            return self.id == other.id

        return False

    @before_event([Replace, Insert])
    def sync_updated_at(self):
        self.updated_at = datetime.now()
