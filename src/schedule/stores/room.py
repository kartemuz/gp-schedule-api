from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Room
from src.schemas import IdSchema


class RoomStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Room]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Room]:
        pass

    @abstractmethod
    async def add(self, obj: Room) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: Room) -> None:
        pass
