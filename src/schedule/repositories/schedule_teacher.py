from typing import Optional, List
from src.schedule.schemas import ScheduleTeacher, ScheduleTeacherInput, ChangeInput
from src.schemas import IdSchema
from src.schedule.stores import ScheduleTeacherStore
from src.schedule.models import ScheduleTeacherDB
from src.utils import DBUtils
from src.schedule.repositories.teacher import teacher_repos
from src.schedule.repositories.change import change_repos
from src.database import session_factory
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload


class ScheduleTeacherRepos(ScheduleTeacherStore):
    async def get(self, id: int) -> Optional[ScheduleTeacher]:
        async with session_factory() as session:
            query = select(ScheduleTeacherDB).where(ScheduleTeacherDB.id == id).options(
                selectinload(ScheduleTeacherDB.change)
            )
            query_result = await session.execute(query)
            schedule_teacher_db = query_result.scalar()

            if schedule_teacher_db:
                result = ScheduleTeacher(
                    id=schedule_teacher_db.id,
                    teacher=await teacher_repos.get(schedule_teacher_db.teacher_id),
                    change=await change_repos.get(schedule_teacher_db.change.id) if schedule_teacher_db.change else None
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[ScheduleTeacher]:
        result: List[ScheduleTeacher] = []
        ids: List[int] = await DBUtils.select_all_id(ScheduleTeacherDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: ScheduleTeacherInput, schedule_id: int) -> IdSchema:
        obj_db = ScheduleTeacherDB(
            id=obj.id,
            teacher_id=obj.teacher.id,
            schedule_id=schedule_id
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(
                ScheduleTeacherDB.id
            ).where(
                and_(
                    ScheduleTeacherDB.teacher_id == obj.teacher.id,
                    ScheduleTeacherDB.schedule_id == schedule_id
                )
            )
            query_result = await session.execute(query)
            result = IdSchema(
                id=query_result.scalar()
            )
        if obj.change:
            await change_repos.add(obj.change, result.id)
        return result

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ScheduleTeacherDB, id)

    async def edit(self, obj: ScheduleTeacherInput, schedule_id: int) -> None:
        obj_db = ScheduleTeacherDB(
            id=obj.id,
            teacher_id=obj.teacher.id,
            schedule_id=schedule_id
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=ScheduleTeacherDB, **data)
        ch = obj.change
        await change_repos.edit(
            obj=ChangeInput(
                id=ch.id,
                teacher=IdSchema(
                    obj.teacher.id
                )
            ),
            schedule_teacher_id=obj.id
        )


schedule_teacher_repos = ScheduleTeacherRepos()
