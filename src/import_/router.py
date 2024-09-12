from fastapi import APIRouter, Depends, File, UploadFile
from src.import_.service import import_service
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.utils import FileUtils

import_router = APIRouter(
    prefix='/import',
    tags=['import']
)


@import_router.post('/teacher')
async def import_teacher(
    file: UploadFile = File(...),
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    path = await FileUtils.save_file(file)
    await import_service.import_teacher(path)
    FileUtils.remove_file(path)


@import_router.post('/type_lesson')
async def import_type_lesson(file: UploadFile = File(...),
                             auth_user: User = Depends(get_auth_active_user)
                             ) -> None:
    path = await FileUtils.save_file(file)
    await import_service.import_type_lesson(path)
    FileUtils.remove_file(path)


@import_router.post('/type_direction')
async def import_type_direction(file: UploadFile = File(...),
                                auth_user: User = Depends(get_auth_active_user)
                                ) -> None:
    path = await FileUtils.save_file(file)
    await import_service.import_type_direction(path)
    FileUtils.remove_file(path)


@import_router.post('/room')
async def import_room(file: UploadFile = File(...),
                      auth_user: User = Depends(get_auth_active_user)
                      ) -> None:
    path = await FileUtils.save_file(file)
    await import_service.import_room(path)
    FileUtils.remove_file(path)
