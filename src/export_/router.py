from fastapi import APIRouter, Depends
from src.export_.service import export_service
from fastapi.responses import FileResponse
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from pathlib import Path
from src.constants import ExportConstants
from src.config import settings
from src.utils import FileUtils

export_router = APIRouter(
    prefix='/export',
    tags=['export']
)


@export_router.get('/teacher')
async def export_teacher(auth_user: User = Depends(get_auth_active_user)) -> FileResponse:
    await FileUtils.create_dir(settings.static.dir_path)
    path: Path = await export_service.export_teacher(settings.static.dir_path)
    return FileResponse(
        path=path,
        filename=path.name,
        media_type=ExportConstants.MEDIA_TYPE
    )


@export_router.get('/discipline')
async def export_discipline(auth_user: User = Depends(get_auth_active_user)) -> FileResponse:
    await FileUtils.create_dir(settings.static.dir_path)
    path: Path = await export_service.export_discipline(settings.static.dir_path)
    return FileResponse(
        path=path,
        filename=path.name,
        media_type=ExportConstants.MEDIA_TYPE
    )


@export_router.get('/direction')
async def export_direction(auth_user: User = Depends(get_auth_active_user)) -> FileResponse:
    await FileUtils.create_dir(settings.static.dir_path)
    path: Path = await export_service.export_direction(settings.static.dir_path)
    return FileResponse(
        path=path,
        filename=path.name,
        media_type=ExportConstants.MEDIA_TYPE
    )


@export_router.get('/group')
async def export_group(auth_user: User = Depends(get_auth_active_user)) -> FileResponse:
    await FileUtils.create_dir(settings.static.dir_path)
    path: Path = await export_service.export_group(settings.static.dir_path)
    return FileResponse(
        path=path,
        filename=path.name,
        media_type=ExportConstants.MEDIA_TYPE
    )


@export_router.get('/schedule')
async def export_schedule(group_id: int, schedule_list_id: int, auth_user: User = Depends(get_auth_active_user)) -> FileResponse:
    await FileUtils.create_dir(settings.static.dir_path)
    path: Path = await export_service.export_schedule(
        group_id,
        schedule_list_id,
        settings.static.dir_path
    )
    return FileResponse(
        path=path,
        filename=path.name,
        media_type=ExportConstants.MEDIA_TYPE
    )
