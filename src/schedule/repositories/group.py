from src.schedule.stores import GroupStore
from typing import Optional, List
from src.schedule.schemas import Group
from src.schedule.models import GroupDB
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database import session_factory


class GroupRepos(GroupStore):
    async def get(self, id: int) -> Optional[Group]:
        pass

    async def get_all(self) -> List[Group]:
        pass

    async def add(self, obj: Group) -> None:
        pass

    async def delete(self, id: int) -> None:
        pass

    async def edit(self, obj: Group) -> None:
        pass
