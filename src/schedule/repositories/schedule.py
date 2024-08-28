from typing import Optional, List
from src.schedule.schemas import Schedule, ScheduleInput
from src.schemas import IdSchema
from src.schedule.stores import ScheduleStore
from src.schedule.models import ScheduleDB
from src.utils import DBUtils
from sqlalchemy import select, and_
from src.database import session_factory
from src.schedule.repositories.schedule_list import schedule_list_repos
from src.schedule.repositories.flow import flow_repos
from src.schedule.repositories.type_lesson import type_lesson_repos
from src.schedule.repositories.discipline import discipline_repos
from src.schedule.repositories.room import room_repos
from src.schedule.repositories.schedule_list import schedule_list_repos


class ScheduleRepos(ScheduleStore):
    async def get(self, id: int) -> Optional[Schedule]:
        async with session_factory() as session:
            query = select(ScheduleDB).where(ScheduleDB.id == id)
            query_result = await session.execute(query)
            schedule_db = query_result.scalar()
            if schedule_db:
                result = Schedule(
                    id=schedule_db.id,
                    date_=schedule_db.date_,
                    time_start=schedule_db.time_start,
                    time_end=schedule_db.time_end,
                    type_lesson=await type_lesson_repos.get(schedule_db.id),
                    flow=await flow_repos.get(schedule_db.flow_id),
                    discipline=await discipline_repos.get(schedule_db.discipline_id),
                    room=await room_repos.get(schedule_db.room_id),
                    schedule_list=await schedule_list_repos.get(schedule_db.schedule_list_id)
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[Schedule]:
        result: List[Schedule] = []
        ids: List[int] = await DBUtils.select_all_id(ScheduleDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: Schedule) -> IdSchema:
        await type_lesson_repos.add(obj.type_lesson)
        await flow_repos.add(obj.flow)
        await discipline_repos.add(obj.discipline)
        await room_repos.add(obj.room)
        await schedule_list_repos.add(obj.schedule_list)
        obj_db = ScheduleDB(
            id=obj.id,
            schedule_list_id=obj.schedule_list.id,
            date_=obj.date_,
            time_start=obj.time_start,
            time_end=obj.time_end,
            type_lesson_id=obj.type_lesson.id,
            flow_id=obj.flow.id,
            discipline_id=obj.discipline.id,
            room_id=obj.room.id
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(
                ScheduleDB.id
            ).where(
                and_(
                    ScheduleDB.schedule_list_id == obj.schedule_list.id,
                    ScheduleDB.date_ == obj.date_,
                    ScheduleDB.time_start == obj.time_start,
                    ScheduleDB.time_end == obj.time_end,
                    ScheduleDB.type_lesson_id == obj.type_lesson.id,
                    ScheduleDB.flow_id == obj.flow.id,
                    ScheduleDB.discipline_id == obj.discipline.id,
                    ScheduleDB.room_id == obj.room.id
                )
            )
            query_result = await session.execute(query)
            id = query_result.scalar()
            return IdSchema(
                id=id
            )

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ScheduleDB, id)

    async def edit(self, obj: Schedule) -> None:
        await self.delete(obj.id)
        await self.add(obj)


schedule_repos = ScheduleRepos()
