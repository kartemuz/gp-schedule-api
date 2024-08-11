from abc import abstractmethod, ABC
from src.core.schemes.user import User
from typing import List


class UserStore(ABC):
    scheme = User

    @abstractmethod
    async def add(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def get(self, login: str) -> scheme:
        pass

    @abstractmethod
    async def edit(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def delete(self, login: str) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[scheme]:
        pass
