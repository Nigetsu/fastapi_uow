__all__ = [
    'v1_task_router',
    'v1_user_router',
]

from src.api.v1.routers.task import router as v1_task_router
from src.api.v1.routers.user import router as v1_user_router
