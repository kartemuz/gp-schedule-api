from abc import abstractmethod, ABC
from src.user.schemas import Action, Entity, Opportunity, Role, User
from typing import List


class ActionStore(ABC):
    @abstractmethod
    async def add(self, obj: Action) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Action:
        pass

    @abstractmethod
    async def get_all(self) -> List[Action]:
        pass


class EntityStore(ABC):
    @abstractmethod
    async def add(self, obj: Entity) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Entity:
        pass

    @abstractmethod
    async def get_all(self) -> List[Entity]:
        pass


class OpportunityStore(ABC):
    @abstractmethod
    async def add(self, obj: Opportunity) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Opportunity:
        pass

    @abstractmethod
    async def get_all(self) -> List[Opportunity]:
        pass


class RoleStore(ABC):
    @abstractmethod
    async def add(self, obj: Role) -> None:
        pass

    @abstractmethod
    async def get(self, name: str) -> Role:
        pass

    @abstractmethod
    async def edit(self, obj: Role) -> None:
        pass

    @abstractmethod
    async def delete(self, name: str) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[Role]:
        pass


class UserStore(ABC):
    @abstractmethod
    async def add(self, obj: User) -> None:
        pass

    @abstractmethod
    async def get(self, login: str) -> User:
        pass

    @abstractmethod
    async def edit(self, obj: User) -> None:
        pass

    @abstractmethod
    async def delete(self, login: str) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass
