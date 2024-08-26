from src.schedule.stores import GroupStore
from typing import Optional, List
from src.schedule.schemas import Group
from src.schemas import IdSchema
from src.schedule.models import GroupDB
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database import session_factory
from src.utils import DBUtils
from sqlalchemy.orm import selectinload
from src.schedule.repositories.direction import direction_repos


class GroupRepos(GroupStore):
    async def get(self, id: int) -> Optional[Group]:
        async with session_factory() as session:
            query = select(GroupDB).where(GroupDB.id == id).options(
                selectinload(GroupDB.direction)
            )
            query_result = await session.execute(query)
            if query_result:
                group_db = query_result.scalar()
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

    async def add(self, obj: Group) -> IdSchema:
        direction_id = await direction_repos.add(obj.direction)
        obj_db = GroupDB(
            id=obj.id,
            direction_id=direction_id,
            number_group=obj.number_group
        )
        await DBUtils.insert_new(obj_db)
        async with session_factory() as session:
            query = select(GroupDB).where(
                GroupDB.number_group == obj.number_group)
            query_result = await session.execute(query)
            obj_db = query_result.scalar()
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(GroupDB, id)

    async def edit(self, obj: Group) -> None:
        await self.delete(obj.id)
        await self.add(obj)


group_repos = GroupRepos()
