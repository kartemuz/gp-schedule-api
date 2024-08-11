from abc import abstractmethod, ABC
from src.core.schemes.user import Action
from typing import List


class ActionStore(ABC):
    scheme = Action

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
