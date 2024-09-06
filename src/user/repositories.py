from src.user.schemas import RoleInput, UserInput, Action, Entity, Opportunity, Role, User
from src.user.stores import (
    ActionStore,
    EntityStore,
    OpportunityStore,
    RoleStore,
    UserStore
)
from src.database import session_factory
from typing import List, Optional
from src.user.models import (
    ActionDB,
    EntityDB,
    OpportunityDB,
    RoleOpportunityDB,
    RoleDB,
    UserDB
)
from sqlalchemy.exc import IntegrityError
from src.utils import DBUtils
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_
from src.schemas import FullName, IdSchema


class ActionRepos(ActionStore):

    async def add(self, obj: Action) -> None:
        action_db = ActionDB(name=obj.name)
        async with session_factory() as session:
            session.add(action_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> Optional[Action]:
        action_db = await DBUtils.select_by_name(model=ActionDB, name=name)
        if action_db:
            result = Action(
                name=action_db.name
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[Action]:
        actions_db: List[ActionDB] = await DBUtils.select_all(ActionDB)
        result = []
        for act in actions_db:
            result.append(
                Action(name=act.name)
            )
        return result


action_repos = ActionRepos()


class EntityRepos(EntityStore):
    async def add(self, obj: Entity) -> None:
        entity_db = EntityDB(name=obj.name)
        async with session_factory() as session:
            session.add(entity_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> Optional[Entity]:
        entity_db = await DBUtils.select_by_name(model=EntityDB, name=name)
        if entity_db:
            result = Entity(name=entity_db.name)
        else:
            result = None
        return result

    async def get_all(self) -> List[Entity]:
        entity_db: List[EntityDB] = await DBUtils.select_all(EntityDB)
        result = []
        for en in entity_db:
            result.append(
                Entity(name=en.name)
            )
        return result


entity_repos = EntityRepos()


class OpportunityRepos(OpportunityStore):
    async def add(self, obj: Opportunity) -> IdSchema:
        # await action_repos.add(obj.action)
        # await entity_repos.add(obj.entity)

        opportunity_db: OpportunityDB = OpportunityDB(
            id=obj.id,
            name=obj.name,
            action_name=obj.action.name,
            entity_name=obj.entity.name
        )

        await DBUtils.insert_new(opportunity_db)
        return IdSchema(id=await DBUtils.select_id_by_name(OpportunityDB, obj.name))

    async def get(self, id: int) -> Optional[Opportunity]:
        async with session_factory() as session:
            query = select(OpportunityDB).where(OpportunityDB.id == id)
            query_result = await session.execute(query)
            if query_result:
                opportunity_db = query_result.scalar()
                result = Opportunity(
                    id=opportunity_db.id,
                    name=opportunity_db.name,
                    action=await action_repos.get(opportunity_db.action_name),
                    entity=await entity_repos.get(opportunity_db.entity_name)
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[Opportunity]:
        result: List[Opportunity] = []
        ids: List[int] = await DBUtils.select_all_id(OpportunityDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result


opportunity_repos = OpportunityRepos()


class RoleRepos(RoleStore):
    async def add(self, obj: RoleInput) -> IdSchema:
        role_db: RoleDB = RoleDB(
            id=obj.id,
            name=obj.name
        )
        await DBUtils.insert_new(role_db)

        for op in obj.opportunities:
            role_opportunity_db: RoleOpportunityDB = RoleOpportunityDB(
                role_id=obj.id,
                opportunity_id=op.id
            )
            await DBUtils.insert_new(role_opportunity_db)
        return IdSchema(id=await DBUtils.select_id_by_name(RoleDB, obj.name))

    async def get(self, id: int) -> Optional[Role]:
        async with session_factory() as session:
            query = select(RoleDB).where(RoleDB.id == id).options(
                selectinload(RoleDB.role_opportunities)
            )
            query_result = await session.execute(query)
            role_db = query_result.scalar()
            if role_db:
                opportunities = []
                for op in role_db.role_opportunities:
                    opportunities.append(
                        await opportunity_repos.get(op.opportunity_id)
                    )

                result = Role(
                    id=role_db.id,
                    name=role_db.name,
                    opportunities=opportunities
                )
            else:
                result = None
        return result

    async def edit(self, obj: RoleInput) -> None:
        await self.delete(name=obj.name)
        await self.add(obj=obj)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(model=RoleDB, id=id)

    async def get_all(self) -> List[Role]:
        result: List[Role] = []
        ids: List[int] = await DBUtils.select_all_id(RoleDB)
        for id in ids:
            result.append(await self.get(id=id))
        return result


role_repos = RoleRepos()


class UserRepos(UserStore):

    async def add(self, obj: UserInput) -> None:
        user_db = UserDB(
            login=obj.login,
            email=obj.email,
            hashed_password=obj.hashed_password,
            surname=obj.full_name.surname,
            name=obj.full_name.name,
            patronymic=obj.full_name.patronymic,
            role_id=obj.role.id
        )
        await DBUtils.insert_new(user_db)

        # async with session_factory() as session:
        #     query = select(UserDB.id).where(UserDB.login == obj.login)
        #     query_result = await session.execute(query)
        #     return query_result.scalar()

    async def get(self, login: str) -> Optional[User]:
        async with session_factory() as session:
            query = select(UserDB).where(UserDB.login == login)
            query_result = await session.execute(query)
            user_db = query_result.scalar()
            if user_db:
                result = User(
                    role=await role_repos.get(user_db.role_id),
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
            else:
                result = None
        return result

    async def edit(self, obj: UserInput) -> None:
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


user_repos = UserRepos()
