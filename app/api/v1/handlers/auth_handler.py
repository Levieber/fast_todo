from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any
from core.schemas.auth_schema import AuthDetail
from core.schemas.user_schema import UserDetail
from core.services.user_service import UserService
from core.models.user_model import User
from infra.token import create_access_token, create_refresh_token
from api.dependencies.user_deps import get_current_user

auth_router = APIRouter()


@auth_router.post(
    "/login", summary="Create access and refresh tokens", response_model=AuthDetail
)
async def login(data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await UserService.authenticate(email=data.username, password=data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail or password incorrect",
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@auth_router.get("/validate", summary="Validate the token", response_model=UserDetail)
async def validate_token(user: User = Depends(get_current_user)):
    return user
