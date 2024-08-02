from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.v1.router import router
from core.models.user_model import User
from core.models.task_model import Task
from infra.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_client = AsyncIOMotorClient(settings.DATABASE_URI, uuidRepresentation="standard")

    await init_beanie(database=db_client.fast_todo, document_models=[User, Task])

    yield

    print("Database connection closed...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_V1_PREFIX)
