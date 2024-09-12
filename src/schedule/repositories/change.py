from typing import Optional, List
from src.schedule.schemas import Change, ChangeInput
from src.schemas import IdSchema
from src.schedule.stores import ChangeStore
from src.schedule.models import ChangeDB
from src.utils import DBUtils
from src.database import session_factory
from sqlalchemy import select, and_
from src.schedule.repositories.teacher import teacher_repos


class ChangeRepos(ChangeStore):
    async def get(self, id: int) -> Optional[Change]:
        schedule_teacher_db: Optional[Change] = await DBUtils.select_by_id(ChangeDB, id)
        if schedule_teacher_db:
            result = Change(
                id=schedule_teacher_db.id,
                teacher=await teacher_repos.get(schedule_teacher_db.teacher_id),
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[Change]:
        result: List[Change] = []
        ids: List[int] = await DBUtils.select_all_id(ChangeDB)
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: ChangeInput, schedule_teacher_id: int) -> IdSchema:

        obj_db = ChangeDB(
            id=obj.id,
            schedule_teacher_id=schedule_teacher_id,
            teacher_id=obj.teacher.id
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(
                ChangeDB.id
            ).where(
                and_(
                    ChangeDB.teacher_id == obj.teacher.id,
                    ChangeDB.schedule_teacher_id == schedule_teacher_id
                )
            )
            query_result = await session.execute(query)
            result = IdSchema(
                id=query_result.scalar()
            )
        return result

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(ChangeDB, id)

    async def edit(self, obj: ChangeInput, schedule_teacher_id: int) -> None:
        obj_db = ChangeDB(
            id=obj.id,
            schedule_teacher_id=schedule_teacher_id,
            teacher_id=obj.teacher.id
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=ChangeDB, **data)


change_repos = ChangeRepos()
