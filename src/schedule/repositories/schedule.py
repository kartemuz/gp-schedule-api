from typing import Optional, List, Set
from src.schedule.schemas import (
    Schedule,
    ScheduleInput,
    ScheduleList,
    ScheduleTeacherInput,
    Flow,
)
from src.schemas import IdSchema
from src.schedule.stores import ScheduleStore
from src.schedule.models import (
    ScheduleDB,
    FlowDB,
    ChangeDB,
    FlowGroupDB,
    ScheduleTeacherDB,
    TeacherDB,
    GroupDB,
)
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
from src.schedule.exc import GroupBusyException, RoomBusyException, TeacherBusyException


class ScheduleRepos(ScheduleStore):
    async def get_by_change_id(self, change_id: int) -> Optional[Schedule]:
        async with session_factory() as session:
            query = (
                select(ScheduleTeacherDB)
                .options(selectinload(ScheduleTeacherDB.change))
                .where(ChangeDB.id == change_id)
            )
            query_result = await session.execute(query)
            s_t_db: Optional[ScheduleTeacherDB] = query_result.scalar()
            if s_t_db:
                result: Schedule = await self.get(s_t_db.schedule_id)
            else:
                result = None
        return result

    async def get_by_schedule_list_id(self, schedule_list_id: int) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = (
                select(ScheduleDB)
                .where(ScheduleDB.schedule_list_id == schedule_list_id)
                .options(selectinload(ScheduleDB.schedule_teachers))
                .order_by(ScheduleDB.date_, ScheduleDB.time_start, ScheduleDB.time_end)
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
                        schedule_list=await schedule_list_repos.get(
                            sc_db.schedule_list_id
                        ),
                        schedule_teachers=schedule_teachers,
                    )
                )
        return result

    async def get_by_time_interval(
        self, time_start: time, time_end: time, date_: date, schedule_list_id: int
    ) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = select(ScheduleDB.id).where(
                and_(
                    ScheduleDB.schedule_list_id == schedule_list_id,
                    ScheduleDB.date_ == date_,
                    ScheduleDB.time_start >= time_start,
                    ScheduleDB.time_end <= time_end,
                )
            )
            query_result = await session.execute(query)
            ids: List[int] = query_result.scalars()
            for id in ids:
                result.append(await self.get(id))
        return result

    async def get_by_group_id(
        self, group_id: int, start_date: str, end_date: str, schedule_list_id: int
    ) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            query = (
                select(ScheduleDB.id)
                .join(FlowDB, FlowDB.id == ScheduleDB.flow_id)
                .join(FlowGroupDB, FlowGroupDB.flow_id == FlowDB.id)
                .filter(
                    FlowGroupDB.group_id == group_id,
                    ScheduleDB.date_.between(start_date, end_date),
                    ScheduleDB.schedule_list_id == schedule_list_id,
                )
                .order_by(ScheduleDB.date_, ScheduleDB.time_start, ScheduleDB.time_end)
            )
            query_result = await session.execute(query)
            schedules_ids_db = query_result.scalars()
            used_id = []
            for id in schedules_ids_db:
                if id not in used_id:
                    result.append(await self.get(id))
                    used_id.append(id)
        return result

    async def get_by_teacher_id(
        self, teacher_id: int, start_date: str, end_date: str, schedule_list_id: int
    ) -> List[Schedule]:
        result: List[Schedule] = []
        async with session_factory() as session:
            # query = select(ScheduleTeacherDB).options(
            #     selectinload(
            #         ScheduleTeacherDB.change
            #     )
            # ).where(
            #     or_(
            #         ScheduleTeacherDB.teacher_id == teacher_id,
            #         ChangeDB.teacher_id == teacher_id
            #     )
            # )

            query = select(ScheduleTeacherDB).where(
                ScheduleTeacherDB.teacher_id == teacher_id
            )

            query_result = await session.execute(query)
            teacher_schedule_ids_list: List[int] = [
                i.schedule_id for i in query_result.scalars()
            ]

            query = select(ChangeDB.schedule_teacher_id).where(
                ChangeDB.teacher_id == teacher_id
            )

            query_result = await session.execute(query)

            s_t_ids = query_result.scalars()
            query = select(ScheduleTeacherDB.schedule_id).where(
                ScheduleTeacherDB.id.in_(s_t_ids)
            )
            query_result = await session.execute(query)

            teacher_schedule_ids_list += [i for i in query_result.scalars()]

            query = select(ScheduleDB.id).where(
                and_(
                    ScheduleDB.date_.between(start_date, end_date),
                    ScheduleDB.schedule_list_id == schedule_list_id,
                )
            )
            query_result = await session.execute(query)
            all_schedule_ids: Set[int] = set(query_result.scalars())

            teacher_schedule_ids: Set[int] = set(teacher_schedule_ids_list)
            good_schedule_ids: Set[int] = all_schedule_ids & teacher_schedule_ids

            for id in good_schedule_ids:
                result.append(await self.get(id))
        return result

    async def get(self, id: int) -> Optional[Schedule]:
        result: Optional[Schedule] = None
        async with session_factory() as session:
            query = (
                select(ScheduleDB)
                .options(selectinload(ScheduleDB.schedule_teachers))
                .where(ScheduleDB.id == id)
            )
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
                    schedule_list=await schedule_list_repos.get(
                        schedule_db.schedule_list_id
                    ),
                    schedule_teachers=schedule_teachers,
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[Schedule]:
        result: List[Schedule] = []
        ids: List[int] = await DBUtils.select_all_id(ScheduleDB)
        for id in ids:
            result.append(await self.get(id))
        return result

    async def add(self, obj: ScheduleInput) -> IdSchema:
        time_end = obj.time_end
        time_start = obj.time_start

        async with session_factory() as session:

            query_by_room_ids = select(ScheduleDB.room_id).filter(
                ScheduleDB.time_end <= time_end,
                ScheduleDB.time_start >= time_start,
                ScheduleDB.schedule_list_id == obj.schedule_list.id,
                ScheduleDB.date_ == obj.date_,
            )
            room_ids_res = await session.execute(query_by_room_ids)
            room_ids = room_ids_res.scalars().all()
            if obj.room.id in room_ids:
                raise RoomBusyException(f"Комната id={obj.room.id} занята")

            query_by_teacher_ids = (
                select(ScheduleTeacherDB.teacher_id)
                .join(ScheduleDB, ScheduleTeacherDB.schedule_id == ScheduleDB.id)
                .filter(
                    ScheduleDB.time_end <= time_end,
                    ScheduleDB.time_start >= time_start,
                    ScheduleDB.schedule_list_id == obj.schedule_list.id,
                    ScheduleDB.date_ == obj.date_,
                )
            )
            teacher_ids_res = await session.execute(query_by_teacher_ids)
            teacher_ids = teacher_ids_res.scalars().all()
            for t in obj.schedule_teachers:
                if t.teacher.id in teacher_ids:
                    raise TeacherBusyException("Учитель id={t.teacher.id} занят")

            query_by_group_ids = (
                select(FlowGroupDB.group_id)
                .select_from(ScheduleDB)
                .join(FlowDB, FlowDB.id == ScheduleDB.flow_id)
                .join(FlowGroupDB, FlowGroupDB.flow_id == FlowDB.id)
                .filter(
                    ScheduleDB.time_end <= time_end,
                    ScheduleDB.time_start >= time_start,
                    ScheduleDB.schedule_list_id == obj.schedule_list.id,
                    ScheduleDB.date_ == obj.date_,
                )
            )
            group_ids_res = await session.execute(query_by_group_ids)
            group_ids = set(group_ids_res.scalars().all())

            query_groups_by_flow = select(FlowGroupDB.group_id).filter(
                FlowGroupDB.flow_id == obj.flow.id
            )
            groups_by_flow_res = await session.execute(query_groups_by_flow)
            groups_by_flow = set(groups_by_flow_res.scalars().all())
            if len(groups_by_flow - group_ids) != len(groups_by_flow):
                raise GroupBusyException("Пересечение рассписания для групп в потоке")

        obj_db = ScheduleDB(
            id=obj.id,
            schedule_list_id=obj.schedule_list.id,
            date_=obj.date_,
            time_start=obj.time_start,
            time_end=obj.time_end,
            type_lesson_id=obj.type_lesson.id,
            flow_id=obj.flow.id,
            discipline_id=obj.discipline.id,
            room_id=obj.room.id,
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(ScheduleDB.id).where(
                and_(
                    ScheduleDB.schedule_list_id == obj.schedule_list.id,
                    ScheduleDB.date_ == obj.date_,
                    ScheduleDB.time_start == obj.time_start,
                    ScheduleDB.time_end == obj.time_end,
                    ScheduleDB.type_lesson_id == obj.type_lesson.id,
                    ScheduleDB.flow_id == obj.flow.id,
                    ScheduleDB.discipline_id == obj.discipline.id,
                    ScheduleDB.room_id == obj.room.id,
                )
            )
            query_result = await session.execute(query)
            result = IdSchema(id=query_result.scalar())
            for s_t in obj.schedule_teachers:
                await schedule_teacher_repos.add(s_t, schedule_id=result.id)
            return result

    async def delete(self, id: int) -> None:
        from sqlalchemy import delete
        from src.database import session_factory
        from src.schedule.models import ScheduleTeacherDB

        async with session_factory() as session:
            stmt = delete(ScheduleTeacherDB).filter(ScheduleTeacherDB.schedule_id == id)
            await session.execute(stmt)

            stmt = delete(ScheduleDB).filter(ScheduleDB.id == id)
            await session.execute(stmt)

            await session.commit()

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
            room_id=obj.room.id,
        )
        data = obj_db.__dict__.copy()
        data.pop("_sa_instance_state")
        await DBUtils.update_by_id(model=ScheduleDB, **data)

        for s_t in obj.schedule_teachers:
            await schedule_teacher_repos.edit(
                obj=ScheduleTeacherInput(
                    id=s_t.id,
                    teacher=IdSchema(s_t.change.teacher.id),
                    change=IdSchema(s_t.change.id),
                ),
                schedule_id=obj.id,
            )

    async def get_by_flow_id(self, flow_id, schedule_list_id) -> list[Schedule]:
        async with session_factory() as session:
            result: list[Schedule] = []
            query = select(ScheduleDB.id).filter(
                ScheduleDB.flow_id == flow_id,
                ScheduleDB.schedule_list_id == schedule_list_id,
            )
            res = await session.execute(query)
            schedule_ids = res.scalars().all()

            for id in schedule_ids:
                result.append(await self.get(id))

            return result


schedule_repos = ScheduleRepos()
