from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List, Set
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Room, FreeObjectInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


room_router = APIRouter(
    prefix='/room',
    tags=ScheduleConstants.TAGS
)


@room_router.post('/get_free')
async def get_free_room(
    data: FreeObjectInput
) -> List[Room]:
    schedules = await schedule_service.schedule_store.get_by_time_interval(
        time_start=data.time_start,
        time_end=data.time_end,
        date_=data.date_,
        schedule_list_id=data.schedule_list_id
    )
    all_rooms = await schedule_service.room_store.get_all()
    all_room_ids: Set[int] = set(
        [r.id for r in all_rooms]
    )
    used_room_ids: Set[int] = set([s.room.id for s in schedules])
    free_room_ids: Set[int] = all_room_ids - used_room_ids
    result: List[Room] = [
        await schedule_service.room_store.get(id) for id in free_room_ids
    ]

    return result


@room_router.get('/get')
async def get_room(
    id: Optional[int] = None
) -> Room | List[Room]:
    if id:
        result: Room = await schedule_service.room_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Room] = await schedule_service.room_store.get_all()
    return result


@room_router.post('/add')
async def add_room(
    room: Room,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.room_store.add(room)


@room_router.post('/edit')
async def edit_room(
    room: Room,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.room_store.edit(room)


@room_router.get('/delete')
async def delete_room(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.room_store.delete(id)
