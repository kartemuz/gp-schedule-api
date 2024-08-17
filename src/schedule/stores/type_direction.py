from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import TypeDirection


class TypeDirectionStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[TypeDirection]:
        pass

    @abstractmethod
    async def get_all() -> List[TypeDirection]:
        pass

    @abstractmethod
    async def add(obj: TypeDirection) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def edit(obj: TypeDirection) -> None:
        pass
