from src.schedule.stores import GroupStore
from typing import Optional, List
from src.schedule.schemas import Group
from src.schedule.models import GroupDB


class GroupRepos(GroupStore):
    async def get(id: int) -> Optional[Group]:
        pass

    async def get_all() -> List[Group]:
        pass

    async def add(obj: Group) -> None:
        pass

    async def delete(id: int) -> None:
        pass

    async def edit(obj: Group) -> None:
        pass
