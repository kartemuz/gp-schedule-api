from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Discipline
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants

discipline_router = APIRouter(
    prefix='/discipline',
    tags=ScheduleConstants.TAGS
)


@discipline_router.get('/get')
async def get_discipline(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> Discipline | List[Discipline]:
    if id:
        result: Discipline = await schedule_service.discipline_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Discipline] = await schedule_service.discipline_store.get_all()
    return result


@discipline_router.post('/add')
async def add_discipline(
    discipline: Discipline,
    auth_user: User = Depends(get_auth_active_user)
) -> IdSchema:
    return await schedule_service.discipline_store.add(discipline)


@discipline_router.post('/edit')
async def edit_discipline(
    discipline: Discipline,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.discipline_store.edit(discipline)


@discipline_router.get('/delete')
async def delete_discipline(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.discipline_store.delete(id)
