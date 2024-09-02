from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Teacher, FreeObjectInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants

teacher_router = APIRouter(
    prefix='/teacher',
    tags=ScheduleConstants.TAGS
)


@teacher_router.post('/search')
async def search_teacher(
    word: str
) -> List[Teacher]:
    result: List[Teacher] = []
    word = word.lower()
    all_teachers = await schedule_service.teacher_store.get_all()
    for t in all_teachers:
        if word in t.full_name.name.lower() or word in t.full_name.surname.lower() or word in t.full_name.patronymic.lower():
            result.append(t)
    return result


@teacher_router.post('/get_free')
async def get_free_teacher(
    data: FreeObjectInput
) -> List[Teacher]:
    pass


@teacher_router.get('/get')
async def get_teacher(
    id: Optional[int] = None
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
