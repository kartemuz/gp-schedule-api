from abc import abstractmethod, ABC
from src.org.schemas import Organization, SocialNetwork
from src.config import settings
from typing import List


class OrgStore(ABC):
    @abstractmethod
    async def add(self, obj: Organization) -> None:
        pass

    @abstractmethod
    async def get(self, name: str = settings.org.name) -> Organization:
        pass

    @abstractmethod
    async def edit(self, obj: Organization) -> None:
        pass

    @abstractmethod
    async def delete(self, name: str = settings.org.name) -> None:
        pass


class SocNetStore(ABC):
    @abstractmethod
    async def add(self, obj: SocialNetwork) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> SocialNetwork:
        pass

    @abstractmethod
    async def edit(self, obj: SocialNetwork) -> None:
        pass

    @abstractmethod
    async def delete(self, name: str) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[SocialNetwork]:
        pass
