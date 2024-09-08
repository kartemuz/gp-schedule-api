from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Group, GroupInput, FlowInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants
from src.config import settings


group_router = APIRouter(
    prefix='/group',
    tags=ScheduleConstants.TAGS
)


@group_router.get('/get')
async def get_group(
    id: Optional[int] = None,
    number_group: Optional[int] = None,
    direction_id: Optional[int] = None
) -> Group | List[Group]:
    if id:
        result: Group = await schedule_service.group_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif number_group:
        result: Group = await schedule_service.group_store.get_by_number_group(number_group)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif direction_id:
        result: List[Group] = await schedule_service.group_store.get_by_direction_id(direction_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Group] = await schedule_service.group_store.get_all()
    return result


@group_router.post('/add')
async def add_group(
    group: GroupInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    group_id = await schedule_service.group_store.add(group)
    await schedule_service.flow_store.add(
        FlowInput(
            id=None,
            name=f'{settings.schedule.base_flow_prefix}_{group_id.id}',
            groups=[
                group_id
            ]
        )
    )

    return group_id


@group_router.post('/edit')
async def edit_group(
    group: GroupInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.edit(group)


@group_router.get('/delete')
async def delete_group(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.delete(id)
    await schedule_service.flow_store.delete_by_name(f'{settings.schedule.base_flow_prefix}_{id}')
