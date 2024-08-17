from src.schedule.stores import TypeDirectionStore
from typing import Optional, List
from src.schedule.schemas import TypeDirection
from src.schedule.models import TypeDirectionDB


class TypeDirectionRepos(TypeDirectionStore):
    async def get(id: int) -> Optional[TypeDirection]:
        pass

    async def get_all() -> List[TypeDirection]:
        pass

    async def add(obj: TypeDirection) -> None:
        pass

    async def delete(id: int) -> None:
        pass

    async def edit(obj: TypeDirection) -> None:
        pass
