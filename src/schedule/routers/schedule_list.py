from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import ScheduleList, ScheduleListInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


schedule_list_router = APIRouter(
    prefix='/schedule_list',
    tags=ScheduleConstants.TAGS
)


@schedule_list_router.get('/get')
async def get_schedule_list(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> ScheduleList | List[ScheduleList]:
    if id:
        result: ScheduleList = await schedule_service.schedule_list_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[ScheduleList] = await schedule_service.schedule_list_store.get_all()
    return result


@schedule_list_router.post('/add')
async def add_schedule_list(
    schedule_list: ScheduleListInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.schedule_list_store.add(schedule_list)


@schedule_list_router.post('/edit')
async def edit_schedule_list(
    schedule_list: ScheduleListInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.schedule_list_store.edit(schedule_list)


@schedule_list_router.get('/delete')
async def delete_schedule_list(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.schedule_list_store.delete(id)
