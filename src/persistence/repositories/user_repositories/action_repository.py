from src.core.stores.user_stores import ActionStore
from src.core.schemes.user import Action
from src.persistence.database.models.user_models import ActionDB
from typing import List
from src.persistence.database.database_utils import BaseQueries
from src.persistence.database import session_factory
from src.persistence.exceptions import IntegrityError


class ActionRepository(ActionStore):
    scheme = Action
    model = ActionDB

    async def add(self, obj: scheme) -> None:
        action_db = self.model(name=obj.name)
        async with session_factory() as session:
            session.add(action_db)
            try:
                await session.commit()

            except IntegrityError as ex:
                await session.rollback()
                # raise ex

    async def get(self, name: str) -> scheme:
        result: self.scheme
        action_db: ActionDB = await BaseQueries.select_by_name(model=self.model, name=name)
        result = self.scheme(name=action_db.name)
        return result

    # async def edit(self, obj: scheme) -> None:
    #     pass

    # async def delete(self, name: str) -> None:
    #     pass

    async def get_all(self) -> List[scheme]:
        action_db: ActionDB = await BaseQueries.select_all(self.model)
        result = []
        for act in action_db:
            result.append(
                Action(name=act.name, value=act.value)
            )
        return result
