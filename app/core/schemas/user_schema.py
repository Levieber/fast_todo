from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="User e-mail")
    username: str = Field(..., min_length=5, max_length=50, description="Username")
    password: str = Field(..., min_length=8, max_length=20, description="User password")


class UserDetail(BaseModel):
    id: UUID
    email: EmailStr
    username: str
