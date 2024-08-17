from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Flow


class FlowStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[Flow]:
        pass

    @abstractmethod
    async def get_all() -> List[Flow]:
        pass

    @abstractmethod
    async def add(obj: Flow) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def edit(obj: Flow) -> None:
        pass
