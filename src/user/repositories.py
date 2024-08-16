from src.user.schemas import Action, Entity, Opportunity, Role, User
from src.user.stores import (
    ActionStore,
    EntityStore,
    OpportunityStore,
    RoleStore,
    UserStore
)
from src.database import session_factory
from typing import List
from src.user.models import (
    ActionDB,
    EntityDB,
    OpportunityDB,
    RoleOpportunityDB,
    RoleDB,
    UserDB
)
from src.exceptions import IntegrityError
from src.utils import DBUtils
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.schemas import FullName


class ActionRepository(ActionStore):

    async def add(self, obj: Action) -> None:
        action_db = ActionDB(name=obj.name)
        async with session_factory() as session:
            session.add(action_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> Action:
        action_db: ActionDB = await DBUtils.select_by_name(model=ActionDB, name=name)
        return Action(
            name=action_db.name
        )

    async def get_all(self) -> List[Action]:
        action_db: List[ActionDB] = await DBUtils.select_all(ActionDB)
        result = []
        for act in action_db:
            result.append(
                Action(name=act.name)
            )
        return result


class EntityRepository(EntityStore):
    async def add(self, obj: Entity) -> None:
        entity_db = EntityDB(name=obj.name)
        async with session_factory() as session:
            session.add(entity_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> Entity:
        entity_db: EntityDB = await DBUtils.select_by_name(model=EntityDB, name=name)
        return Entity(name=entity_db.name)

    async def get_all(self) -> List[Entity]:
        entity_db: List[EntityDB] = await DBUtils.select_all(EntityDB)
        result = []
        for en in entity_db:
            result.append(
                Entity(name=en.name)
            )
        return result


class OpportunityRepository(OpportunityStore):

    async def add(self, obj: Opportunity) -> None:
        async with session_factory() as session:
            await ActionRepository().add(Action)
            await EntityRepository().add(Entity)

            opportunity_db: OpportunityDB = OpportunityDB(
                name=obj.name,
                action_name=obj.action.name,
                entity_name=obj.entity.name
            )

            session.add(opportunity_db)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> Opportunity:
        async with session_factory() as session:
            query = select(OpportunityDB).where(OpportunityDB.name == name).options(
                selectinload(OpportunityDB.action),
                selectinload(OpportunityDB.entity)
            )
            query_result = await session.execute(query)
            opportunity_db = query_result.scalar()
            return Opportunity(
                name=opportunity_db.name,
                action=Action(name=opportunity_db.action.name),
                entity=Entity(name=opportunity_db.entity.name)
            )

    async def get_all(self) -> List[Opportunity]:
        result: List[Opportunity] = []

        async with session_factory() as session:
            query = select(OpportunityDB).options(
                selectinload(OpportunityDB.action),
                selectinload(OpportunityDB.entity)
            )
            query_result = await session.execute(query)
            opportunities_db: List[OpportunityDB] = query_result.scalars()

            for op_db in opportunities_db:
                result.append(
                    Opportunity(
                        name=op_db.name,
                        action=Action(name=op_db.action.name),
                        entity=Entity(name=op_db.entity.name)
                    )
                )

        return result


class RoleRepository(RoleStore):
    async def add(self, obj: Role) -> None:
        for op in obj.opportunities:
            await OpportunityRepository().add(op)

        async with session_factory() as session:
            role_db: RoleDB = RoleDB(
                name=obj.name
            )
            session.add(role_db)
            for op in obj.opportunities:
                role_opportunity_db: RoleOpportunityDB = RoleOpportunityDB(
                    role_name=obj.name,
                    opportunity_name=op.name
                )
                session.add(role_opportunity_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> Role:
        async with session_factory() as session:
            query = select(RoleDB).where(RoleDB.name == name).options(
                selectinload(RoleDB.role_opportunities).selectinload(
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

            return Role(
                name=role_db.name,
                opportunities=opportunities
            )

    async def edit(self, obj: Role) -> None:
        await self.delete(name=obj.name)
        await self.add(obj=obj)

    async def delete(self, name: str) -> None:
        await DBUtils.delete_by_name(model=RoleDB, name=name)

    async def get_all(self) -> List[Role]:
        result: List[Role] = []
        all_names = await DBUtils.select_all_name(RoleDB)
        for name in all_names:
            result.append(await self.get(name=name))
        return result


class UserRepository(UserStore):

    async def add(self, obj: User) -> None:
        if obj.role:
            await RoleRepository().add(obj=obj.role)
            role_name = obj.role.name
        else:
            role_name = None
        async with session_factory() as session:
            user_db = UserDB(
                login=obj.login,
                email=obj.email,
                hashed_password=obj.hashed_password,
                surname=obj.full_name.surname,
                name=obj.full_name.name,
                patronymic=obj.full_name.patronymic,
                role_name=role_name
            )

            session.add(user_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, login: str) -> User:
        async with session_factory() as session:
            query = select(UserDB).where(UserDB.login == login)
            query_result = await session.execute(query)
            user_db = query_result.scalar()
            role = await RoleRepository().get(name=user_db.role_name)
            return User(
                role=role,
                login=user_db.login,
                email=user_db.email,
                hashed_password=user_db.hashed_password,
                full_name=FullName(
                    surname=user_db.surname,
                    name=user_db.name,
                    patronymic=user_db.patronymic
                ),
                active=user_db.active
            )

    async def edit(self, obj: User) -> None:
        await self.delete(login=obj.login)
        await self.add(obj=obj)

    async def delete(self, login: str) -> None:
        async with session_factory() as session:

            query_user = select(UserDB).where(UserDB.login == login)
            qeury_user_result = await session.execute(query_user)
            user_db = qeury_user_result.scalar()

            await session.delete(user_db)
            await session.commit()

    async def get_all(self) -> List[User]:
        result: List[User] = []
        async with session_factory() as session:
            query_all_logins = select(UserDB.login)
            query_all_logins_result = await session.execute(query_all_logins)
            all_logins_db: List[str] = query_all_logins_result.scalars()
        for login in all_logins_db:
            result.append(
                await self.get(login=login)
            )
        return result
