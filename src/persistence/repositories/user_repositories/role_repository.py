from src.core.stores.user_stores import RoleStore
from src.core.schemes.user import Role, Opportunity, Action, Entity
from src.persistence.database.models.user_models import RoleDB, RoleOpportunityDB, OpportunityDB
from typing import List
from src.persistence.database.database_utils import BaseQueries
from src.persistence.database import session_factory
from src.persistence.exceptions import IntegrityError
from src.persistence.repositories.user_repositories import OpportunityRepository
from sqlalchemy.orm import selectinload
from sqlalchemy import select


class RoleRepository(RoleStore):
    scheme = Role
    model = RoleDB

    async def add(self, obj: scheme) -> None:
        for op in obj.opportunities:
            await OpportunityRepository().add(op)

        async with session_factory() as session:
            role_db: self.model = self.model(
                name=obj.name
            )
            session.add(role_db)
            for op in obj.opportunities:
                role_opportunity_db = RoleOpportunityDB(
                    role_name=obj.name,
                    opportunity_name=op.name
                )
                session.add(role_opportunity_db)
            try:
                await session.commit()

            except IntegrityError as ex:
                await session.rollback()
                # raise ex

    async def get(self, name: str) -> scheme:
        result: self.scheme
        async with session_factory() as session:
            query = select(self.model).where(self.model.name == name).options(
                selectinload(self.model.role_opportunities).selectinload(
                    RoleOpportunityDB.opportunity
                )
            )
            query_result = await session.execute(query)
            role_db = query_result.scalar()

            opportunities = []
            for op in role_db.role_opportunities:
                opportunities.append(
                    Opportunity(
                        name=op.opportunity.name,
                        action=Action(name=op.opportunity.action.name),
                        entity=Entity(name=op.opportunity.entity.name)
                    )
                )

            result: self.scheme = self.scheme(
                name=role_db.name,
                opportunities=opportunities
            )
        return result

    async def edit(self, obj: scheme) -> None:
        await self.delete(name=obj.name)
        await self.add(obj=obj)

    async def delete(self, name: str) -> None:
        await BaseQueries.delete_by_name(model=self.model, name=name)

    async def get_all(self) -> List[scheme]:
        result: List[Role] = []
        all_names = await BaseQueries.select_all_name(self.model)
        for name in all_names:
            result.append(await self.get(name=name))
        return result
