from fastapi import APIRouter, HTTPException, status, Depends
from typing import Final, Optional, List
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.schedule.schemas import (
    TypeDirection,
    Group,
    Discipline,
    Direction,
    Flow,
    Teacher
)
from src.schedule.service import schedule_service

tags: Final = ['schedule']

schedule_router = APIRouter(
    prefix='/schedule',
    tags=tags,
)

group_router = APIRouter(
    prefix='/group',
    tags=tags
)


@group_router.get('/get')
async def get_group(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> Group | List[Group]:
    if id:
        result: Group = await schedule_service.group_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Group] = await schedule_service.group_store.get_all()
    return result


@group_router.post('/add')
async def add_group(
    group: Group,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.add(group)


@group_router.post('/edit')
async def edit_group(
    group: Group,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.edit(group)


@group_router.get('/delete')
async def delete_group(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.group_store.delete(id)

flow_router = APIRouter(
    prefix='/flow',
    tags=tags
)


@flow_router.get('/get')
async def get_flow(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> Flow | List[Flow]:
    if id:
        result: Flow = await schedule_service.flow_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Flow] = await schedule_service.flow_store.get_all()
    return result


@flow_router.post('/add')
async def add_flow(
    flow: Flow,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.flow_store.add(flow)


@flow_router.post('/edit')
async def edit_flow(
    flow: Flow,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.flow_store.edit(flow)


@flow_router.get('/delete')
async def delete_flow(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.flow_store.delete(id)

discipline_router = APIRouter(
    prefix='/discipline',
    tags=tags
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
) -> None:
    await schedule_service.discipline_store.add(discipline)


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

teacher_router = APIRouter(
    prefix='/teacher',
    tags=tags
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
) -> None:
    await schedule_service.teacher_store.add(teacher)


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

type_direction_router = APIRouter(
    prefix='/type_direction',
    tags=tags
)


@type_direction_router.get('/get')
async def get_type_direction(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> TypeDirection | List[TypeDirection]:
    if id:
        result: TypeDirection = await schedule_service.type_direction_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[TypeDirection] = await schedule_service.type_direction_store.get_all()
    return result


@type_direction_router.post('/add')
async def add_type_direction(
    type_direction: TypeDirection,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_direction_store.add(type_direction)


@type_direction_router.post('/edit')
async def edit_type_direction(
    type_direction: TypeDirection,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_direction_store.edit(type_direction)


@type_direction_router.get('/delete')
async def delete_type_direction(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.type_direction_store.delete(id)


direction_router = APIRouter(
    prefix='/direction',
    tags=tags
)


@direction_router.get('/get')
async def get_direction(
    id: Optional[int] = None,
    auth_user: User = Depends(get_auth_active_user)
) -> Direction | List[Direction]:
    if id:
        result: Direction = await schedule_service.direction_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result: List[Direction] = await schedule_service.direction_store.get_all()
    return result


@direction_router.post('/add')
async def add_direction(
    direction: Direction,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.direction_store.add(direction)


@direction_router.post('/edit')
async def edit_direction(
    direction: Direction,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.direction_store.edit(direction)


@direction_router.get('/delete')
async def delete_direction(
    id: int,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    await schedule_service.direction_store.delete(id)


routers = (
    group_router,
    flow_router,
    discipline_router,
    teacher_router,
    type_direction_router,
    direction_router
)

for r in routers:
    schedule_router.include_router(r)
