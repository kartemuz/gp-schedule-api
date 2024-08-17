from src.schedule.stores import DisciplineStore
from typing import Optional, List
from src.schedule.schemas import Discipline
from src.schedule.models import DisciplineDB


class DisciplineRepos(DisciplineStore):
    async def get(id: int) -> Optional[Discipline]:
        pass

    async def get_all() -> List[Discipline]:
        pass

    async def add(obj: Discipline) -> None:
        pass

    async def delete(id: int) -> None:
        pass

    async def edit(obj: Discipline) -> None:
        pass
