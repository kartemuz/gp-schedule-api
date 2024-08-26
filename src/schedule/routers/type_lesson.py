from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import TypeLesson
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


type_lesson_router = APIRouter(
    prefix='/type_lesson',
    tags=ScheduleConstants.TAGS
)


@type_lesson_router.get('/get')
async def get_type_lesson(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> TypeLesson | List[TypeLesson]:
    if id:
        result: TypeLesson = await schedule_service.type_lesson_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[TypeLesson] = await schedule_service.type_lesson_store.get_all()
    return result


@type_lesson_router.post('/add')
async def add_type_lesson(
    type_lesson: TypeLesson,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.type_lesson_store.add(type_lesson)


@type_lesson_router.post('/edit')
async def edit_type_lesson(
    type_lesson: TypeLesson,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_lesson_store.edit(type_lesson)


@type_lesson_router.get('/delete')
async def delete_type_lesson(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_lesson_store.delete(id)
