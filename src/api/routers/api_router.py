from fastapi import APIRouter
from .organization_router import organization_router

api_router = APIRouter(
    prefix="/api"
)

routers_list = (
    organization_router
)

for r in routers_list:
    api_router.include_router(organization_router)
