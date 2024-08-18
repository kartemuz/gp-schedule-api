from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Teacher


class TeacherStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[Teacher]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Teacher]:
        pass

    @abstractmethod
    async def add(self, obj: Teacher) -> None:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: Teacher) -> None:
        pass
