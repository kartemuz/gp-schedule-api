from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Discipline


class DisciplineStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[Discipline]:
        pass

    @abstractmethod
    async def get_all() -> List[Discipline]:
        pass

    @abstractmethod
    async def add(obj: Discipline) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def edit(obj: Discipline) -> None:
        pass
