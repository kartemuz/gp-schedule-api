from abc import ABC, abstractmethod
from src.schedule.schemas import LoadList, LoadListInput
from src.schemas import IdSchema
from typing import Optional, List


class LoadListStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[LoadList]:
        pass

    @abstractmethod
    async def get_all(self) -> List[LoadList]:
        pass

    @abstractmethod
    async def add(self, obj: LoadListInput) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: LoadListInput) -> None:
        pass
