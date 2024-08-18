from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Discipline


class DisciplineStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Discipline]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Discipline]:
        pass

    @abstractmethod
    async def add(self, obj: Discipline) -> None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: Discipline) -> None:
        pass
