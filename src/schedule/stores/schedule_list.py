from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import ScheduleList, ScheduleListInput
from src.schemas import IdSchema


class ScheduleListStore(ABC):
    @abstractmethod
    async def get_active(sefl) -> Optional[ScheduleList]:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[ScheduleList]:
        pass

    @abstractmethod
    async def get_all(self) -> List[ScheduleList]:
        pass

    @abstractmethod
    async def add(self, obj: ScheduleListInput) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: ScheduleListInput) -> None:
        pass
