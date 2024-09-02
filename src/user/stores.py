from abc import abstractmethod, ABC
from src.user.schemas import RoleInput, UserInput, Action, Entity, Opportunity, Role, User
from typing import List, Optional


class ActionStore(ABC):
    @abstractmethod
    async def add(self, obj: Action) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Optional[Action]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Action]:
        pass


class EntityStore(ABC):
    @abstractmethod
    async def add(self, obj: Entity) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Optional[Entity]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Entity]:
        pass


class OpportunityStore(ABC):
    @abstractmethod
    async def add(self, obj: Opportunity) -> int:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[Opportunity]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Opportunity]:
        pass


class RoleStore(ABC):
    @abstractmethod
    async def add(self, obj: RoleInput) -> int:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[Role]:
        pass

    @abstractmethod
    async def edit(self, obj: RoleInput) -> None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[Role]:
        pass


class UserStore(ABC):
    @abstractmethod
    async def add(self, obj: UserInput) -> int:
        pass

    @abstractmethod
    async def get(self, login: str) -> Optional[User]:
        pass

    @abstractmethod
    async def edit(self, obj: UserInput) -> None:
        pass

    @abstractmethod
    async def delete(self, login: str) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass
