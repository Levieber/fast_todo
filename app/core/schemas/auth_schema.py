from uuid import UUID
from pydantic import BaseModel


class AuthDetail(BaseModel):
    access_token: str
    refresh_token: str


class AuthPayload(BaseModel):
    sub: UUID
    exp: int
