from fastapi import APIRouter
from .organization_router import organization_router
from .auth_router import auth_router
from .user_router import user_router

api_router = APIRouter(
    prefix="/api"
)

routers_list = (
    organization_router,
    auth_router,
    user_router,
)

for r in routers_list:
    api_router.include_router(r)
