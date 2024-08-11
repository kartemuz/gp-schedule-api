from src.core.stores.user_stores import OpportunityStore
from src.core.schemes.user import Opportunity, Action, Entity
from src.persistence.database.models.user_models import OpportunityDB
from typing import List
from src.persistence.database import session_factory
from src.persistence.exceptions import IntegrityError
from src.persistence.repositories.user_repositories import ActionRepository, EntityRepository
from sqlalchemy.orm import selectinload
from sqlalchemy import select


class OpportunityRepository(OpportunityStore):
    scheme = Opportunity
    model = OpportunityDB

    async def add(self, obj: scheme) -> None:
        async with session_factory() as session:
            await ActionRepository().add(obj.action)
            await EntityRepository().add(obj.entity)

            opportunity_db: OpportunityDB = self.model(
                name=obj.name,
                action_name=obj.action.name,
                entity_name=obj.entity.name
            )

            session.add(opportunity_db)
            try:
                await session.commit()

            except IntegrityError as ex:
                await session.rollback()
                # raise ex

    async def get(self, name: str) -> scheme:
        result: self.scheme
        async with session_factory() as session:
            query = select(self.model).where(self.model.name == name).options(
                selectinload(self.model.action),
                selectinload(self.model.entity)
            )
            query_result = await session.execute(query)
            opportunity_db = query_result.scalar()
            result = self.scheme(
                name=opportunity_db.name,
                action=Action(name=opportunity_db.action.name),
                entity=Entity(name=opportunity_db.entity.name)
            )
        return result

    async def get_all(self) -> List[scheme]:
        result: List[self.scheme] = []

        async with session_factory() as session:
            query = select(self.model).options(
                selectinload(self.model.action),
                selectinload(self.model.entity)
            )
            query_result = await session.execute(query)
            opportunities_db: List[OpportunityDB] = query_result.scalars()

            for op_db in opportunities_db:
                result.append(
                    self.scheme(
                        name=op_db.name,
                        action=Action(name=op_db.action.name),
                        entity=Entity(name=op_db.entity.name)
                    )
                )

        return result
