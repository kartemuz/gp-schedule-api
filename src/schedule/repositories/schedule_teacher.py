from typing import Optional, List
from src.schedule.schemas import ScheduleTeacher
from src.schemas import IdSchema
from src.schedule.stores import ScheduleTeacherStore
from src.schedule.models import ScheduleTeacherDB
from src.utils import DBUtils
from src.schedule.repositories.teacher import teacher_repos
from src.schedule.repositories.schedule import schedule_repos
from src.database import session_factory
from sqlalchemy import select


class ScheduleTeacherRepos(ScheduleTeacherStore):
    async def get(self, id: int) -> Optional[ScheduleTeacher]:
        schedule_teacher_db: Optional[ScheduleTeacher] = await DBUtils.select_by_id(ScheduleTeacherDB, id)
        if schedule_teacher_db:
            result = ScheduleTeacher(
                id=schedule_teacher_db.id,
                teacher=await teacher_repos.get(schedule_teacher_db.teacher_id),
                schedule=await teacher_repos.get(schedule_teacher_db.schedule_id)
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[ScheduleTeacher]:
        result: List[ScheduleTeacher] = []
        ids: List[int] = DBUtils.select_all_id(ScheduleTeacherDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: ScheduleTeacher) -> IdSchema:
        await teacher_repos.add(obj.teacher)
        await schedule_repos.add(obj.schedule)
        obj_db = ScheduleTeacherDB(
            id=obj.id,
            teacher_id=obj.teacher.id,
            schedule_id=obj.schedule.id
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(
                ScheduleTeacherDB.id
            ).where(
                ScheduleTeacherDB.teacher_id == obj.teacher.id,
                ScheduleTeacherDB.schedule_id == obj.schedule.id
            )
            query_result = await session.execute(query)
            id = query_result.scalar()
            return IdSchema(
                id=id
            )

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ScheduleTeacherDB, id)

    async def edit(self, obj: ScheduleTeacher) -> None:
        await self.delete(obj.id)
        await self.add(obj)


schedule_teacher_repos = ScheduleTeacherRepos()
