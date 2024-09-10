from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import TeacherLoadList, TeacherLoadListInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


teacher_load_list_router = APIRouter(
    prefix='/teacher_load_list',
    tags=ScheduleConstants.TAGS
)


@teacher_load_list_router.get('/get')
async def get_teacher_load_list(
    id: Optional[int] = None,
    load_list_id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> TeacherLoadList | List[TeacherLoadList]:
    if id:
        result: TeacherLoadList = await schedule_service.teacher_load_list_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    elif load_list_id:
        pass
    else:
        result: List[TeacherLoadList] = await schedule_service.teacher_load_list_store.get_all()
    return result


@teacher_load_list_router.post('/add')
async def add_teacher_load_list(
    teacher_load_list: TeacherLoadListInput,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.teacher_load_list_store.add(teacher_load_list)


@teacher_load_list_router.post('/edit')
async def edit_teacher_load_list(
    teacher_load_list: TeacherLoadListInput,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.teacher_load_list_store.edit(teacher_load_list)


@teacher_load_list_router.get('/delete')
async def delete_teacher_load_list(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.teacher_load_list_store.delete(id)
