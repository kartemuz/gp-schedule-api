from abc import abstractmethod, ABC
from src.core.schemes.organization import Organization
from src.config import settings


class OrganizationStore(ABC):
    scheme = Organization

    @abstractmethod
    async def add(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def get(self, name: str = settings.ORGANIZATION_NAME) -> scheme:
        pass

    @abstractmethod
    async def edit(self, obj: scheme) -> None:
        pass

    @abstractmethod
    async def delete(self, name: str = settings.ORGANIZATION_NAME) -> None:
        pass
