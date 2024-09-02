from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Schedule
from src.schemas import IdSchema


class ScheduleStore(ABC):
    @abstractmethod
    async def get_by_teacher_id_and_date(self, teacher_id: int, start_date: str, end_date: str) -> List[Schedule]:
        pass

    @abstractmethod
    async def get_by_group_id_and_date(self, group_id: int, start_date: str, end_date: str) -> List[Schedule]:
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
