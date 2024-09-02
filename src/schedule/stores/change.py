from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Change, ChangeInput
from src.schemas import IdSchema


class ChangeStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Change]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Change]:
        pass

    @abstractmethod
    async def add(self, obj: ChangeInput, schedule_teacher_id: int) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: ChangeInput, schedule_teacher_id: int) -> None:
        pass
