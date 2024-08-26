from abc import ABC, abstractmethod
from typing import Optional, List
from src.schedule.schemas import TypeLesson
from src.schemas import IdSchema


class TypeLessonStore(ABC):
    @abstractmethod
    async def get(self, id: int) -> Optional[TypeLesson]:
        pass

    @abstractmethod
    async def get_all(self) -> List[TypeLesson]:
        pass

    @abstractmethod
    async def add(self, obj: TypeLesson) -> IdSchema:
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        pass

    @abstractmethod
    async def edit(self, obj: TypeLesson) -> None:
        pass
