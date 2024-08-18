from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import TypeDirection


class TypeDirectionStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[TypeDirection]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TypeDirection]:
        pass

    @abstractmethod
    async def add(self, obj: TypeDirection) -> None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: TypeDirection) -> None:
        pass
