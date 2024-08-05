from src.core.stores.user_stores import ActionStore
from src.core.schemes.user import Action
from typing import Optional, List


STORE = ActionStore
SCHEME = Action


class ActionRepository(STORE):
    async def add(obj: SCHEME) -> None:
        pass

    async def get(id: Optional[int] = None, name: Optional[str] = None) -> Optional[SCHEME]:
        pass

    async def edit(obj: SCHEME) -> None:
        pass

    async def delete(id: Optional[int] = None, name: Optional[str] = None) -> None:
        pass

    async def get_all() -> List[SCHEME]:
        pass
