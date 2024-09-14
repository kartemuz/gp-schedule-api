from typing import Optional, List
from src.schedule.schemas import Schedule, ScheduleInput, ScheduleList
from src.schemas import IdSchema
from src.schedule.stores import ScheduleStore
from src.schedule.models import ScheduleDB, FlowDB, ChangeDB, FlowGroupDB, ScheduleTeacherDB, TeacherDB
from src.utils import DBUtils
from sqlalchemy import select, and_, or_
from src.database import session_factory
from src.schedule.repositories.schedule_list import schedule_list_repos
from src.schedule.repositories.flow import flow_repos
from src.schedule.repositories.type_lesson import type_lesson_repos
from src.schedule.repositories.discipline import discipline_repos
from src.schedule.repositories.room import room_repos
from src.schedule.repositories.schedule_teacher import schedule_teacher_repos
from sqlalchemy.orm import selectinload
from datetime import time, date


class ScheduleRepos(ScheduleStore):
    async def get_by_schedule_list_id(self, schedule_list_id: int) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = select(ScheduleDB).where(
                ScheduleDB.schedule_list_id == schedule_list_id
            ).options(
                selectinload(
                    ScheduleDB.schedule_teachers
                )
            )
            query_result = await session.execute(query)
            schedules_db: List[ScheduleDB] = query_result.scalars()

            for sc_db in schedules_db:
                schedule_teachers = []
                for s_t_db in sc_db.schedule_teachers:
                    schedule_teachers.append(
                        await schedule_teacher_repos.get(s_t_db.id)
                    )
                result.append(
                    Schedule(
                        id=sc_db.id,
                        date_=sc_db.date_,
                        time_start=sc_db.time_start,
                        time_end=sc_db.time_end,
                        type_lesson=await type_lesson_repos.get(sc_db.type_lesson_id),
                        flow=await flow_repos.get(sc_db.flow_id),
                        discipline=await discipline_repos.get(sc_db.discipline_id),
                        room=await room_repos.get(sc_db.room_id),
                        schedule_list=await schedule_list_repos.get(sc_db.schedule_list_id),
                        schedule_teachers=schedule_teachers
                    )
                )
        return result

    async def get_by_time_interval(self, time_start: time, time_end: time, date_: date, schedule_list_id: int) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = select(ScheduleDB.id).where(
                and_(
                    ScheduleDB.schedule_list_id == schedule_list_id,
                    ScheduleDB.date_ == date_,
                    ScheduleDB.time_start >= time_start,
                    ScheduleDB.time_end <= time_end
                )
            )
            query_result = await session.execute(query)
            ids: List[int] = query_result.scalars()
            for id in ids:
                result.append(
                    await self.get(id)
                )
        return result

    async def get_by_group_id_and_date(self, group_id: int, start_date: str, end_date: str) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = select(ScheduleDB).options(
                selectinload(ScheduleDB.flow).selectinload(FlowDB.flows_groups)
            ).where(
                and_(
                    FlowGroupDB.group_id == group_id,
                    ScheduleDB.date_.between(start_date, end_date)
                )
            )
            query_result = await session.execute(query)
            schedules_db = query_result.scalars()
            used_id = []
            for sc_db in schedules_db:
                if sc_db.id not in used_id:
                    result.append(
                        await self.get(sc_db.id)
                    )
                used_id.append(sc_db.id)
        return result

    async def get_by_teacher_id_and_date(self, teacher_id: int, start_date: str, end_date: str) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = select(ScheduleDB).options(
                selectinload(
                    ScheduleDB.schedule_teachers
                ).selectinload(
                    ScheduleTeacherDB.teacher
                ),

                selectinload(
                    ScheduleDB.schedule_teachers
                ).selectinload(
                    ScheduleTeacherDB.change
                )
            ).where(
                and_(
                    or_(
                        TeacherDB.id == teacher_id,
                        ChangeDB.teacher_id == teacher_id
                    ),

                    ScheduleDB.date_.between(start_date, end_date)
                )
            )
            query_result = await session.execute(query)
            schedules_db = query_result.scalars()
            for sc_db in schedules_db:
                schedule_teachers = []
                for s_t_db in sc_db.schedule_teachers:
                    schedule_teachers.append(
                        await schedule_teacher_repos.get(s_t_db.id)
                    )
                result.append(
                    Schedule(
                        id=sc_db.id,
                        date_=sc_db.date_,
                        time_start=sc_db.time_start,
                        time_end=sc_db.time_end,
                        type_lesson=await type_lesson_repos.get(sc_db.type_lesson_id),
                        flow=await flow_repos.get(sc_db.flow_id),
                        discipline=await discipline_repos.get(sc_db.discipline_id),
                        room=await room_repos.get(sc_db.room_id),
                        schedule_list=await schedule_list_repos.get(sc_db.schedule_list_id),
                        schedule_teachers=schedule_teachers
                    )
                )
        return result

    async def get(self, id: int) -> Optional[Schedule]:
        result: Optional[Schedule] = None
        async with session_factory() as session:
            query = select(ScheduleDB).options(
                selectinload(
                    ScheduleDB.schedule_teachers
                )
            ).where(ScheduleDB.id == id)
            query_result = await session.execute(query)
            schedule_db = query_result.scalar()
            if schedule_db:
                schedule_teachers = []
                for s_t_db in schedule_db.schedule_teachers:
                    schedule_teachers.append(
                        await schedule_teacher_repos.get(s_t_db.id)
                    )
                result = Schedule(
                    id=schedule_db.id,
                    date_=schedule_db.date_,
                    time_start=schedule_db.time_start,
                    time_end=schedule_db.time_end,
                    type_lesson=await type_lesson_repos.get(schedule_db.type_lesson_id),
                    flow=await flow_repos.get(schedule_db.flow_id),
                    discipline=await discipline_repos.get(schedule_db.discipline_id),
                    room=await room_repos.get(schedule_db.room_id),
                    schedule_list=await schedule_list_repos.get(schedule_db.schedule_list_id),
                    schedule_teachers=schedule_teachers
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

    async def add(self, obj: ScheduleInput) -> IdSchema:

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
            result = IdSchema(
                id=query_result.scalar()
            )
            for s_t in obj.schedule_teachers:
                await schedule_teacher_repos.add(s_t, schedule_id=result.id)
            return result

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ScheduleDB, id)

    async def edit(self, obj: Schedule) -> None:
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
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=ScheduleDB, **data)


schedule_repos = ScheduleRepos()
