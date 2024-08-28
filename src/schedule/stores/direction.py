from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Direction, DirectionInput
from src.schemas import IdSchema


class DirectionStore(ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Direction]:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[Direction]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Direction]:
        pass

    @abstractmethod
    async def add(self, obj: DirectionInput) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: DirectionInput) -> None:
        pass
