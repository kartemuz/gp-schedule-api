from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import ScheduleTeacher, ScheduleTeacherInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


schedule_teacher_router = APIRouter(
    prefix='/schedule_teacher',
    tags=ScheduleConstants.TAGS
)


@schedule_teacher_router.get('/get')
async def get_schedule_teacher(
    id: Optional[int] = None
) -> ScheduleTeacher | List[ScheduleTeacher]:
    if id:
        result: ScheduleTeacher = await schedule_service.schedule_teacher_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[ScheduleTeacher] = await schedule_service.schedule_teacher_store.get_all()
    return result


# @schedule_teacher_router.post('/add')
# async def add_schedule_teacher(
#     schedule_teacher: ScheduleTeacherInput,
#     auth_user: User = Depends(get_auth_active_user)
# ) -> IdSchema:
#     return await schedule_service.schedule_teacher_store.add(schedule_teacher)


# @schedule_teacher_router.post('/edit')
# async def edit_schedule_teacher(
#     schedule_teacher: ScheduleTeacherInput,
#     auth_user: User = Depends(get_auth_active_user)
# ) -> None:
#     await schedule_service.schedule_teacher_store.edit(schedule_teacher)


@schedule_teacher_router.get('/delete')
async def delete_schedule_teacher(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.schedule_teacher_store.delete(id)
