from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import LoadList, LoadListInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


load_list_router = APIRouter(
    prefix='/load_list',
    tags=ScheduleConstants.TAGS
)


@load_list_router.get('/get')
async def get_load_list(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> LoadList | List[LoadList]:
    if id:
        result: LoadList = await schedule_service.load_list_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[LoadList] = await schedule_service.load_list_store.get_all()
    return result


@load_list_router.post('/add')
async def add_load_list(
    load_list: LoadListInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.load_list_store.add(load_list)


@load_list_router.post('/edit')
async def edit_load_list(
    load_list: LoadListInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.load_list_store.edit(load_list)


@load_list_router.get('/delete')
async def delete_load_list(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.load_list_store.delete(id)
