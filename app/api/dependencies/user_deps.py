from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from datetime import datetime
from pydantic import ValidationError
from core.services.user_service import UserService
from core.models.user_model import User
from core.schemas.auth_schema import AuthPayload
from infra.config import settings
from infra.token import decode_token
import jwt

oauth_config = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login", scheme_name="JWT"
)


async def get_current_user(token: str = Depends(oauth_config)) -> User:
    try:
        payload = decode_token(token)
        token_data = AuthPayload(**payload)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_by_id(token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
