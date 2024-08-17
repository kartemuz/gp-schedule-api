from src.schedule.stores import FlowStore
from typing import Optional, List
from src.schedule.schemas import Flow
from src.schedule.models import FlowDB


class FlowRepos(FlowStore):
    async def get(id: int) -> Optional[Flow]:
        pass

    async def get_all() -> List[Flow]:
        pass

    async def add(obj: Flow) -> None:
        pass

    async def delete(id: int) -> None:
        pass

    async def edit(obj: Flow) -> None:
        pass
