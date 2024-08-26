from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Teacher
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants

teacher_router = APIRouter(
    prefix='/teacher',
    tags=ScheduleConstants.TAGS
)


@teacher_router.get('/get')
async def get_teacher(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> Teacher | List[Teacher]:
    if id:
        result: Teacher = await schedule_service.teacher_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Teacher] = await schedule_service.teacher_store.get_all()
    return result


@teacher_router.post('/add')
async def add_teacher(
    teacher: Teacher,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.teacher_store.add(teacher)


@teacher_router.post('/edit')
async def edit_teacher(
    teacher: Teacher,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.teacher_store.edit(teacher)


@teacher_router.get('/delete')
async def delete_teacher(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.teacher_store.delete(id)
