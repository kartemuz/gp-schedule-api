from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import ScheduleTeacher, ScheduleTeacherInput
from src.schemas import IdSchema


class ScheduleTeacherStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[ScheduleTeacher]:
        pass

    @abstractmethod
    async def get_all(self) -> List[ScheduleTeacher]:
        pass

    @abstractmethod
    async def add(self, obj: ScheduleTeacherInput, schedule_id: int) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: ScheduleTeacherInput, schedule_id: int) -> None:
        pass
