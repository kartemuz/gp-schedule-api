from abc import abstractmethod, ABC
from src.core.schemes.organization import SocialNetwork
from typing import Optional, List


class SocialNetworkStore(ABC):
    scheme = SocialNetwork

    @abstractmethod
    async def add(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Optional[scheme]:
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
