from openpyxl import Workbook
from pathlib import Path
from src.config import settings
from pathlib import Path
from src.constants import ExportConstants
from src.schedule.service import schedule_service


class ExportService:
    async def export_teacher(self, dir_path: Path) -> Path:
        path: Path = dir_path / \
            f'export_teacher.{ExportConstants.FILE_EXTENSION}'

        return path

    async def export_direction(self, dir_path: Path) -> Path:
        path: Path = dir_path / \
            f'export_direction.{ExportConstants.FILE_EXTENSION}'

        return path

    async def export_discipline(self, dir_path: Path) -> Path:
        path: Path = dir_path / \
            f'export_discipline.{ExportConstants.FILE_EXTENSION}'

        return path

    async def export_group(self, dir_path: Path) -> Path:
        path: Path = dir_path / \
            f'export_group.{ExportConstants.FILE_EXTENSION}'

        return path

    async def export_schedule(self, dir_path: Path) -> Path:
        path: Path = dir_path / \
            f'export_schedule.{ExportConstants.FILE_EXTENSION}'

        return path


export_service = ExportService()
