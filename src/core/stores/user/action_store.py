from abc import abstractmethod, ABC
from src.core.schemes.user import Action


SCHEME = Action


class ActionStore(ABC):
    @abstractmethod
    async def add():
        pass

    @abstractmethod
    async def get() -> SCHEME:
        pass

    @abstractmethod
    async def edit():
        pass

    @abstractmethod
    async def delete():
        pass

    @abstractmethod
    async def get_all():
        pass
