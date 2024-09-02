from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import Change, ChangeInput
from src.schemas import IdSchema
from src.schedule.service import schedule_service
from src.constants import ScheduleConstants


change_router = APIRouter(
    prefix='/change',
    tags=ScheduleConstants.TAGS
)


@change_router.get('/get')
async def get_change(
    id: Optional[int] = None
) -> Change | List[Change]:
    if id:
        result: Change = await schedule_service.change_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Change] = await schedule_service.change_store.get_all()
    return result


# @change_router.post('/add')
# async def add_change(
#     change: ChangeInput,
#     auth_user: User = Depends(get_auth_active_user)
# ) -> IdSchema:
#     return await schedule_service.change_store.add(change)


# @change_router.post('/edit')
# async def edit_change(
#     change: ChangeInput,
#     auth_user: User = Depends(get_auth_active_user)
# ) -> None:
#     await schedule_service.change_store.edit(change)


@change_router.get('/delete')
async def delete_change(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.change_store.delete(id)
