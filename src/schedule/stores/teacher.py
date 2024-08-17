from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import Teacher


class TeacherStore(ABC):
    @abstractmethod
    async def get(id: int) -> Optional[Teacher]:
        pass

    @abstractmethod
    async def get_all() -> List[Teacher]:
        pass

    @abstractmethod
    async def add(obj: Teacher) -> None:
        pass

    @abstractmethod
    async def delete(id: int) -> None:
        pass

    @abstractmethod
    async def edit(obj: Teacher) -> None:
        pass
