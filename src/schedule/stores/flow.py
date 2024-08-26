from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Flow
from src.schemas import IdSchema


class FlowStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Flow]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Flow]:
        pass

    @abstractmethod
    async def add(self, obj: Flow) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: Flow) -> None:
        pass
