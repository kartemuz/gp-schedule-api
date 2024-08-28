from typing import Optional, List
from src.schedule.schemas import ScheduleList, ScheduleListInput
from src.schemas import IdSchema
from src.schedule.stores import ScheduleListStore
from src.utils import DBUtils
from src.schedule.models import ScheduleListDB
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database import session_factory
from src.schedule.repositories.load_list import load_list_repos


class ScheduleListRepos(ScheduleListStore):
    async def get(self, id: int) -> Optional[ScheduleList]:
        async with session_factory() as session:
            query = select(ScheduleListDB).where(ScheduleListDB.id == id).options(
                selectinload(ScheduleListDB.load_list)
            )
            query_result = await session.execute(query)
            schedule_list_db = query_result.scalar()
            if schedule_list_db:
                load_list = await load_list_repos.get(schedule_list_db.load_list.id)
                result = ScheduleList(
                    id=schedule_list_db.id,
                    name=schedule_list_db.name,
                    date_start=schedule_list_db.date_start,
                    date_end=schedule_list_db.date_end,
                    active=schedule_list_db.active,
                    load_list=load_list
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[ScheduleList]:
        result: List[ScheduleList] = []
        ids: List[int] = await DBUtils.select_all_id(ScheduleListDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: ScheduleListInput) -> IdSchema:
        obj_db = ScheduleListDB(
            id=obj.id,
            name=obj.name,
            date_start=obj.date_start,
            date_end=obj.date_end,
            load_list_id=obj.load_list.id,
            active=obj.active
        )
        await DBUtils.insert_new(obj_db)
        async with session_factory() as session:
            query = select(
                ScheduleListDB.id
            ).where(ScheduleListDB.name == obj.name)
            query_result = await session.execute(query)
            id = query_result.scalar()
            return IdSchema(
                id=id
            )

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ScheduleListDB, id)

    async def edit(self, obj: ScheduleListInput) -> None:
        await self.delete(obj.id)
        await self.add(obj)


schedule_list_repos = ScheduleListRepos()
