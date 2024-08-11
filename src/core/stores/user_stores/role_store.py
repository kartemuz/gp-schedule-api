from abc import abstractmethod, ABC
from src.core.schemes.user import Role
from typing import List


class RoleStore(ABC):
    scheme = Role

    @abstractmethod
    async def add(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> scheme:
        pass

    @abstractmethod
    async def edit(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def delete(self, name: str) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[scheme]:
        pass
