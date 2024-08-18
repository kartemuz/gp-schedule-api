from src.schedule.stores import FlowStore
from typing import Optional, List
from src.schedule.schemas import Flow
from src.schedule.models import FlowDB
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database import session_factory


class FlowRepos(FlowStore):
    async def get(self, id: int) -> Optional[Flow]:
        pass

    async def get_all(self) -> List[Flow]:
        pass

    async def add(self, obj: Flow) -> None:
        pass

    async def delete(self, id: int) -> None:
        pass

    async def edit(self, obj: Flow) -> None:
        pass
