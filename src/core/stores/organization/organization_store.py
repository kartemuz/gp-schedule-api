from abc import abstractmethod, ABC
from src.core.schemes.organization import Organization
from typing import Optional, List


SCHEME = Organization


class OrganizationStore(ABC):
    @abstractmethod
    async def add(obj: SCHEME) -> None:
        pass

    @abstractmethod
    async def get(id: int) -> Optional[SCHEME]:
        pass

    @abstractmethod
    async def edit(obj: SCHEME) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def get_all() -> List[SCHEME]:
        pass
