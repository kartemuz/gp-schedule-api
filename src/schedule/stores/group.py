from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Group


class GroupStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[Group]:
        pass

    @abstractmethod
    async def get_all() -> List[Group]:
        pass

    @abstractmethod
    async def add(obj: Group) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def edit(obj: Group) -> None:
        pass
