from src.schedule.stores import TeacherStore
from typing import Optional, List
from src.schedule.schemas import Teacher
from src.schedule.models import TeacherDB


class TeacherRepos(TeacherStore):
    async def get(id: int) -> Optional[Teacher]:
        pass

    async def get_all() -> List[Teacher]:
        pass

    async def add(obj: Teacher) -> None:
        pass

    async def delete(id: int) -> None:
        pass

    async def edit(obj: Teacher) -> None:
        pass
