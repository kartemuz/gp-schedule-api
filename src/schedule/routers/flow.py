from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Flow, FlowInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants
from src.config import settings


flow_router = APIRouter(
    prefix='/flow',
    tags=ScheduleConstants.TAGS
)


@flow_router.get('/get_base_flow')
async def get_base_flow(id: Optional[int] = None) -> Flow | List[Flow]:
    if id:
        result: Flow = await schedule_service.flow_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        flows: List[Flow] = await schedule_service.flow_store.get_all()
        result: List[Flow] = []
        for f in flows:
            if settings.schedule.base_flow_prefix in f.name:
                result.append(f)
    return result


@flow_router.get('/get')
async def get_flow(
    id: Optional[int] = None
) -> Flow | List[Flow]:
    if id:
        result: Flow = await schedule_service.flow_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Flow] = await schedule_service.flow_store.get_all()
        for r in result:
            if settings.schedule.base_flow_prefix in r.name:
                result.remove(r)
    return result


@flow_router.post('/add')
async def add_flow(
    flow: FlowInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.flow_store.add(flow)


@flow_router.post('/edit')
async def edit_flow(
    flow: FlowInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.flow_store.edit(flow)


@flow_router.get('/delete')
async def delete_flow(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.flow_store.delete(id)
