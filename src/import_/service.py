from openpyxl import Workbook
from pathlib import Path
from src.config import settings
from pathlib import Path
from src.schedule.service import schedule_service


class ImportService:
    async def import_teacher(self, paht: Path) -> None:
        pass

    async def import_type_lesson(self, path: Path) -> None:
        pass

    async def import_type_direction(self, path: Path) -> None:
        pass


import_service = ImportService()
