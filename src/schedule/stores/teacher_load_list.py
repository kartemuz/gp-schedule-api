from abc import ABC, abstractmethod
from src.schedule.schemas import TeacherLoadList
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
    async def add(self, obj: TeacherLoadList, load_list_id: int) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: TeacherLoadList, load_list_id: int) -> None:
        pass
