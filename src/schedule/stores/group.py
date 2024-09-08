from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Group, GroupInput
from src.schemas import IdSchema


class GroupStore(ABC):

    @staticmethod
    async def get_by_direction_id(self, direction_id: int) -> List[Group]:
        pass

    @abstractmethod
    async def get_by_number_group(self, number_group: str) -> Optional[Group]:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[Group]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Group]:
        pass

    @abstractmethod
    async def add(self, obj: GroupInput) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: GroupInput) -> None:
        pass
