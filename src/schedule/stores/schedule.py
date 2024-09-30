from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Schedule
from src.schemas import IdSchema
from datetime import time, date


class ScheduleStore(ABC):
    @abstractmethod
    async def get_by_change_id(self, change_id: int) -> Optional[Schedule]:
        pass

    @abstractmethod
    async def get_by_schedule_list_id(self, schedule_list_id: int) -> List[Schedule]:
        pass

    @abstractmethod
    async def get_by_time_interval(self, time_start: time, time_end: time, date_: date, schedule_list_id: int) -> List[Schedule]:
        pass

    @abstractmethod
    async def get_by_teacher_id(self, teacher_id: int, start_date: str, end_date: str, schedule_list_id: int) -> List[Schedule]:
        pass

    @abstractmethod
    async def get_by_group_id(self, group_id: int, start_date: str, end_date: str, schedule_list_id: int) -> List[Schedule]:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[Schedule]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Schedule]:
        pass

    @abstractmethod
    async def add(self, obj: Schedule) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: Schedule) -> None:
        pass
