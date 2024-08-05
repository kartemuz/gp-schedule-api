from abc import abstractmethod, ABC
from src.core.schemes.user import Role
from typing import Optional, List


SCHEME = Role


class RoleStore(ABC):
    @abstractmethod
    async def add(obj: SCHEME) -> None:
        pass

    @abstractmethod
    async def get(id: Optional[int] = None, name: Optional[str] = None) -> Optional[SCHEME]:
        pass

    @abstractmethod
    async def edit(obj: SCHEME) -> None:
        pass

    @abstractmethod
    async def delete(id: Optional[int] = None, name: Optional[str] = None) -> None:
        pass

    @abstractmethod
    async def get_all() -> List[SCHEME]:
        pass
