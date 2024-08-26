from fastapi import APIRouter
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

schedule_router = APIRouter(
    prefix='/schedule',
    tags=['schedule'],
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
)

for r in routers:
    schedule_router.include_router(r)
