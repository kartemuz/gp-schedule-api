from abc import ABC, abstractmethod
from src.schedule.schemas import TeacherLoadList, TeacherLoadListInput
from src.schemas import IdSchema
from typing import Optional, List


class TeacherLoadListStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[TeacherLoadList]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TeacherLoadList]:
        pass

    @abstractmethod
    async def add(self, obj: TeacherLoadListInput) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: TeacherLoadList) -> None:
        pass
