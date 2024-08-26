from typing import Optional, List
from src.schedule.schemas import Change
from src.schemas import IdSchema
from src.schedule.stores import ChangeStore
from src.schedule.models import ChangeDB
from src.utils import DBUtils
from src.database import session_factory
from sqlalchemy import select
from src.schedule.repositories.teacher import teacher_repos
from src.schedule.repositories.schedule_teacher import schedule_teacher_repos


class ChangeRepos(ChangeStore):
    async def get(self, id: int) -> Optional[Change]:
        schedule_teacher_db: Optional[Change] = await DBUtils.select_by_id(ChangeDB, id)
        if schedule_teacher_db:
            result = Change(
                id=schedule_teacher_db.id,
                teacher=await teacher_repos.get(schedule_teacher_db.teacher_id),
                schedule_teacher=await teacher_repos.get(schedule_teacher_db.schedule_id)
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[Change]:
        result: List[Change] = []
        ids: List[int] = DBUtils.select_all_id(ChangeDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: Change) -> IdSchema:
        await teacher_repos.add(obj.teacher)
        await schedule_teacher_repos.add(obj.schedule_teacher)

        obj_db = ChangeDB(
            id=obj.id,
            schedule_teacher_id=obj.schedule_teacher.id,
            teacher_id=obj.teacher.id
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(
                ChangeDB.id
            ).where(
                ChangeDB.teacher_id == obj.teacher.id,
                ChangeDB.schedule_teacher_id == obj.schedule_teacher.id
            )
            query_result = await session.execute(query)
            id = query_result.scalar()
            return IdSchema(
                id=id
            )

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ChangeDB, id)

    async def edit(self, obj: Change) -> None:
        await self.delete(obj.id)
        await self.add(obj)
