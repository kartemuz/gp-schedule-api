from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Group
from src.schemas import IdSchema


class GroupStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Group]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Group]:
        pass

    @abstractmethod
    async def add(self, obj: Group) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: Group) -> None:
        pass
