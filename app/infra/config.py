from typing import List
from decouple import config
from pydantic import AnyHttpUrl, TypeAdapter
from pydantic_settings import BaseSettings

UrlTypeAdapter = TypeAdapter(AnyHttpUrl)


class Settings(BaseSettings):
    API_V1_PREFIX: str = "/api/v1"
    JWT_SECRET: str = str(config("JWT_SECRET"))
    JWT_REFRESH_SECRET: str = str(config("JWT_REFRESH_SECRET"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    CORS_ORIGINS: List[AnyHttpUrl] = [
        UrlTypeAdapter.validate_python("http://localhost:3000")
    ]
    PROJECT_NAME: str = "FastToDo"
    DATABASE_URI: str = str(config("DATABASE_URI"))

    class Config:
        case_sensitive = True


settings = Settings()
