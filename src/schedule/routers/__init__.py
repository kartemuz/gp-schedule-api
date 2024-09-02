from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List, Final
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Schedule, ScheduleInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants
from datetime import timedelta, datetime

from .group import group_router
from .direction import direction_router
from .discipline import discipline_router
from .flow import flow_router
from .teacher import teacher_router
from .type_direction import type_direction_router
from .type_lesson import type_lesson_router
from .load_list import load_list_router
from .room import room_router
from .teacher_load_list import teacher_load_list_router
from .schedule_list import schedule_list_router
from .schedule_teacher import schedule_teacher_router
from .change import change_router

schedule_router = APIRouter(
    prefix='/schedule',
    tags=ScheduleConstants.TAGS,
)

routers = (
    group_router,
    direction_router,
    discipline_router,
    flow_router,
    teacher_router,
    type_direction_router,
    type_lesson_router,
    load_list_router,
    room_router,
    teacher_load_list_router,
    schedule_list_router,
    schedule_teacher_router,
    change_router
)

DATE_FORMAT: Final = '%Y-%m-%d'


def get_cur_str_date():
    today = datetime.today()
    return (today - timedelta(days=today.weekday())).date().strftime(DATE_FORMAT)


@schedule_router.get('/get')
async def get_schedule(
    id: Optional[int] = None,
    group_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    start_of_week: Optional[str] = get_cur_str_date()
) -> Schedule | List[Schedule]:

    start_of_week = datetime.strptime(start_of_week, DATE_FORMAT)
    end_of_week = (start_of_week + timedelta(days=6))

    if id:
        result: Schedule = await schedule_service.schedule_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif group_id:
        result: Schedule = await schedule_service.schedule_store.get_by_group_id_and_date(

        )
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    elif teacher_id:
        result: Schedule = await schedule_service.schedule_store.get_by_teacher_id_and_date(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    else:
        result: List[Schedule] = await schedule_service.schedule_store.get_all()
    return result


@schedule_router.post('/add')
async def add_schedule(
    schedule: ScheduleInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.schedule_store.add(schedule)


@schedule_router.post('/edit')
async def edit_schedule(
    schedule: ScheduleInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.schedule_store.edit(schedule)


@schedule_router.get('/delete')
async def delete_schedule(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.schedule_store.delete(id)

for r in routers:
    schedule_router.include_router(r)