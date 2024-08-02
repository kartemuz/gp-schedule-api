from abc import abstractmethod, ABC
from src.core.schemes.user import Opportunity
from typing import Optional, List


SCHEME = Opportunity


class OpportunityStore(ABC):
    @abstractmethod
    async def add() -> None:
        pass

    @abstractmethod
    async def get(id: Optional[int] = None, name: Optional[str] = None) -> SCHEME:
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
