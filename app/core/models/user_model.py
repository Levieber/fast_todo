from beanie import Document, Indexed
from uuid import UUID, uuid4
from pydantic import Field, EmailStr
from typing_extensions import Annotated
from typing import Optional


class User(Document):
    id: UUID = Field(default_factory=uuid4)
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    password: str

    @classmethod
    async def by_email(cls, email: str) -> Optional["User"]:
        return await cls.find_one(cls.email == email)

    def __repr__(self) -> str:
        return f"User {self.email}"

    def __str__(self) -> str:
        return self.email

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email

        return False
