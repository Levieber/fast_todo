import pymongo.errors
from fastapi import APIRouter, HTTPException, status
from core.schemas.user_schema import UserRegister, UserDetail
from core.services.user_service import UserService

user_router = APIRouter()


@user_router.post("/", summary="Create an user", response_model=UserDetail)
async def index_users(data: UserRegister):
    try:
        return await UserService.create(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or e-mail already exists",
        )
