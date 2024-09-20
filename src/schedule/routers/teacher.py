from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List, Set
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Teacher, FreeObjectInput, TeacherLoadList
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
) -> List[TeacherLoadList]:
    result: List[TeacherLoadList] = []
    schedules = await schedule_service.schedule_store.get_by_time_interval(
        time_start=data.time_start,
        time_end=data.time_end,
        date_=data.date_,
        schedule_list_id=data.schedule_list_id
    )
    schedule_list = await schedule_service.schedule_list_store.get(data.schedule_list_id)
    all_teacher_ids: Set[int] = set(
        [t_l.teacher.id for t_l in schedule_list.load_list.teacher_load_lists]
    )

    used_teacher_ids = []
    for s in schedules:
        schedule_teachers = s.schedule_teachers
        for s_t in schedule_teachers:
            change = s_t.change
            if change:
                used_teacher_ids.append(
                    change.teacher.id
                )
            else:
                used_teacher_ids.append(
                    s_t.teacher.id
                )
    used_teacher_ids: Set[int] = set(used_teacher_ids)
    free_teacher_ids: Set[int] = all_teacher_ids - used_teacher_ids

    for t_l in schedule_list.load_list.teacher_load_lists:
        if t_l.teacher.id in free_teacher_ids:
            result.append(t_l)
    return result


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
