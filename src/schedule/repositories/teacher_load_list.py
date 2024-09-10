from src.schedule.stores import TeacherLoadListStore
from src.schedule.schemas import TeacherLoadList, TeacherLoadListInput
from src.schemas import IdSchema
from src.schedule.models import TeacherLoadListDB
from typing import Optional, List
from src.utils import DBUtils
from src.schedule.repositories.teacher import teacher_repos
from src.database import session_factory
from sqlalchemy import select, and_


class TeacherLoadListRepos(TeacherLoadListStore):
    async def get(self, id: int) -> Optional[TeacherLoadList]:
        teacher_load_list_db: Optional[TeacherLoadListDB] = await DBUtils.select_by_id(TeacherLoadListDB, id)
        if teacher_load_list_db:
            result = TeacherLoadList(
                id=teacher_load_list_db.id,
                hours=teacher_load_list_db.hours,
                teacher=await teacher_repos.get(id=teacher_load_list_db.teacher_id)
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[TeacherLoadList]:
        ids = await DBUtils.select_all_id(TeacherLoadListDB)
        result: List[TeacherLoadList] = []
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: TeacherLoadListInput) -> IdSchema:
        obj_db = TeacherLoadListDB(
            id=obj.id,
            load_list_id=obj.load_list.id,
            teacher_id=obj.teacher.id,
            hours=obj.hours
        )
        await DBUtils.insert_new(obj_db)
        async with session_factory() as session:
            query = select(TeacherLoadListDB).where(
                and_(
                    TeacherLoadListDB.hours == obj.hours,
                    TeacherLoadListDB.load_list_id == obj.load_list.id,
                    TeacherLoadListDB.teacher_id == obj.teacher.id
                )
            )
            query_result = await session.execute(query)
            obj_db = query_result.scalar()
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TeacherLoadListDB, id)

    async def edit(self, obj: TeacherLoadListInput) -> None:
        obj_db = TeacherLoadListDB(
            id=obj.id,
            load_list_id=obj.load_list.id,
            teacher_id=obj.teacher.id,
            hours=obj.hours
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=TeacherLoadListDB, **data)


teacher_load_list_repos = TeacherLoadListRepos()
