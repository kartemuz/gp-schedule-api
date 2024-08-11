from abc import abstractmethod, ABC
from src.core.schemes.user import Entity
from typing import List


class EntityStore(ABC):
    scheme = Entity

    @abstractmethod
    async def add(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> scheme:
        pass

    # @abstractmethod
    # async def edit(self, obj: scheme) -> None:
    #     pass

    # @abstractmethod
    # async def delete(self, name: str) -> None:
    #     pass

    @abstractmethod
    async def get_all(self) -> List[scheme]:
        pass
