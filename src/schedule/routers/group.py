from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Group
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


group_router = APIRouter(
    prefix='/group',
    tags=ScheduleConstants.TAGS
)


@group_router.get('/get')
async def get_group(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> Group | List[Group]:
    if id:
        result: Group = await schedule_service.group_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Group] = await schedule_service.group_store.get_all()
    return result


@group_router.post('/add')
async def add_group(
    group: Group,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.group_store.add(group)


@group_router.post('/edit')
async def edit_group(
    group: Group,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.edit(group)


@group_router.get('/delete')
async def delete_group(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.delete(id)
