from src.schedule.stores import GroupStore
from typing import Optional, List
from src.schedule.schemas import Group, GroupInput
from src.schemas import IdSchema
from src.schedule.models import GroupDB
from sqlalchemy import select
from src.database import session_factory
from src.utils import DBUtils
from sqlalchemy.orm import selectinload
from src.schedule.repositories.direction import direction_repos


class GroupRepos(GroupStore):

    async def get_by_direction_id(self, direction_id: int) -> List[Group]:
        async with session_factory() as session:
            result: List[Group] = []
            query = select(GroupDB).where(GroupDB.direction_id == direction_id).options(
                selectinload(GroupDB.direction)
            )
            query_result = await session.execute(query)
            groups_db = query_result.scalars()
            for g_db in groups_db:
                direction = await direction_repos.get(id=g_db.direction.id)
                result.append(
                    Group(
                        id=g_db.id,
                        number_group=g_db.number_group,
                        direction=direction
                    )
                )
        return result

    async def get_by_number_group(self, number_group: str) -> Optional[Group]:
        async with session_factory() as session:
            query = select(GroupDB).where(GroupDB.number_group == number_group).options(
                selectinload(GroupDB.direction)
            )
            query_result = await session.execute(query)
            group_db = query_result.scalar()
            if group_db:
                direction = await direction_repos.get(id=group_db.direction.id)
                result = Group(
                    id=group_db.id,
                    number_group=group_db.number_group,
                    direction=direction
                )
            else:
                result = None
        return result

    async def get(self, id: int) -> Optional[Group]:
        async with session_factory() as session:
            query = select(GroupDB).where(GroupDB.id == id).options(
                selectinload(GroupDB.direction)
            )
            query_result = await session.execute(query)
            group_db = query_result.scalar()
            if group_db:
                direction = await direction_repos.get(id=group_db.direction.id)
                result = Group(
                    id=group_db.id,
                    number_group=group_db.number_group,
                    direction=direction
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[Group]:
        ids = await DBUtils.select_all_id(GroupDB)
        result: List[Group] = []
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: GroupInput) -> IdSchema:
        obj_db = GroupDB(
            id=obj.id,
            direction_id=obj.direction.id,
            number_group=obj.number_group
        )
        print(obj.id, obj.direction.id, obj.number_group)
        await DBUtils.insert_new(obj_db)
        async with session_factory() as session:
            query = select(GroupDB.id).where(
                GroupDB.number_group == obj.number_group)
            query_result = await session.execute(query)
            id: int = query_result.scalar()
            return IdSchema(id=id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(GroupDB, id)

    async def edit(self, obj: GroupInput) -> None:
        obj_db = GroupDB(
            id=obj.id,
            direction_id=obj.direction.id,
            number_group=obj.number_group
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=GroupDB, **data)


group_repos = GroupRepos()
