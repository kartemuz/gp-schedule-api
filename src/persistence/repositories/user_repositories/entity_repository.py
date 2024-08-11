from src.core.stores.user_stores import EntityStore
from src.core.schemes.user import Entity
from src.persistence.database.models.user_models import EntityDB
from typing import List
from src.persistence.database.database_utils import BaseQueries
from src.persistence.database import session_factory
from src.persistence.exceptions import IntegrityError


class EntityRepository(EntityStore):
    scheme = Entity
    model = EntityDB

    async def add(self, obj: scheme) -> None:
        entity_db = self.model(name=obj.name)
        async with session_factory() as session:
            session.add(entity_db)
            try:
                await session.commit()

            except IntegrityError as ex:
                await session.rollback()
                # raise ex

    async def get(self, name: str) -> scheme:
        result: self.scheme
        entity_db: EntityDB = await BaseQueries.select_by_name(model=self.model, name=name)
        result = self.scheme(name=entity_db.name)
        return result

    # async def edit(self, obj: scheme) -> None:
    #     pass

    # async def delete(self, name: str) -> None:
    #     pass

    async def get_all(self) -> List[scheme]:
        entity_db: EntityDB = await BaseQueries.select_all(self.model)
        result = []
        for act in entity_db:
            result.append(
                Entity(name=act.name, value=act.value)
            )
        return result
