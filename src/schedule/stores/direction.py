from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Direction


class DirectionStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[Direction]:
        pass

    @abstractmethod
    async def get_all() -> List[Direction]:
        pass

    @abstractmethod
    async def add(obj: Direction) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def edit(obj: Direction) -> None:
        pass
