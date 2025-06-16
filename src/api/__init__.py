from fastapi import APIRouter

from src.api.v1.routers import v1_task_router, v1_user_router

router = APIRouter()

router.include_router(v1_user_router, prefix='/v1', tags=['User | v1'])
router.include_router(v1_task_router, prefix='/v1', tags=['Task | v1'])
