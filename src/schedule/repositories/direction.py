from src.schedule.stores import DirectionStore
from typing import Optional, List
from src.schedule.schemas import Direction
from src.schedule.models import DirectionDB


class DirectionRepos(DirectionStore):
    async def get(id: int) -> Optional[Direction]:
        pass

    async def get_all() -> List[Direction]:
        pass

    async def add(obj: Direction) -> None:
        pass

    async def delete(id: int) -> None:
        pass

    async def edit(obj: Direction) -> None:
        pass
