from typing import Optional, Union, Any
from datetime import datetime, timedelta, timezone
import jwt
from infra.config import settings


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[int] = None
) -> str:
    now = datetime.now(timezone.utc)

    if expires_delta is not None:
        expires_delta = int(datetime.timestamp(now + timedelta(minutes=expires_delta)))
    else:
        expires_delta = int(
            datetime.timestamp(
                now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
        )

    payload = {"exp": expires_delta, "sub": str(subject)}

    return jwt.encode(payload, settings.JWT_SECRET, settings.ALGORITHM)


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[int] = None
) -> str:
    now = datetime.now(timezone.utc)

    if expires_delta is not None:
        expires_delta = int(datetime.timestamp(now + timedelta(minutes=expires_delta)))
    else:
        expires_delta = int(
            datetime.timestamp(
                now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            )
        )

    payload = {"exp": expires_delta, "sub": str(subject)}

    return jwt.encode(payload, settings.JWT_REFRESH_SECRET, settings.ALGORITHM)


def decode_token(token: str) -> Any:
    return jwt.decode(token, settings.JWT_SECRET, [settings.ALGORITHM])
