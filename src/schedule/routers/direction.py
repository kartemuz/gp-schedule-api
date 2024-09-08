from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Direction, DirectionInput, TypeDirection, Discipline
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


direction_router = APIRouter(
    prefix='/direction',
    tags=ScheduleConstants.TAGS
)


@direction_router.get('/get')
async def get_direction(
    id: Optional[int] = None,
    name: Optional[str] = None
) -> Direction | List[Direction]:
    if id:
        result: Direction = await schedule_service.direction_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif name:
        result: Direction = await schedule_service.direction_store.get_by_name(name)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Direction] = await schedule_service.direction_store.get_all()

    return result


@direction_router.post('/add')
async def add_direction(
    direction: DirectionInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.direction_store.add(direction)


@direction_router.post('/edit')
async def edit_direction(
    direction: DirectionInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.direction_store.edit(direction)


@direction_router.get('/delete')
async def delete_direction(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.direction_store.delete(id)
