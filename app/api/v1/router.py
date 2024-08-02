from fastapi import APIRouter
from .handlers.user_handler import user_router
from .handlers.auth_handler import auth_router
from .handlers.task_handler import task_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(task_router, prefix="/tasks", tags=["tasks"])
