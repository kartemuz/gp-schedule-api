from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import TypeDirection
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


type_direction_router = APIRouter(
    prefix='/type_direction',
    tags=ScheduleConstants.TAGS
)


@type_direction_router.get('/get')
async def get_type_direction(
    id: Optional[int] = None
) -> TypeDirection | List[TypeDirection]:
    if id:
        result: TypeDirection = await schedule_service.type_direction_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[TypeDirection] = await schedule_service.type_direction_store.get_all()
    return result


@type_direction_router.post('/add')
async def add_type_direction(
    type_direction: TypeDirection,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.type_direction_store.add(type_direction)


@type_direction_router.post('/edit')
async def edit_type_direction(
    type_direction: TypeDirection,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_direction_store.edit(type_direction)


@type_direction_router.get('/delete')
async def delete_type_direction(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_direction_store.delete(id)
