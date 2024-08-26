from src.schedule.stores import TeacherLoadListStore
from src.schedule.schemas import TeacherLoadList
from src.schemas import IdSchema
from src.schedule.models import TeacherLoadListDB
from typing import Optional, List
from src.utils import DBUtils
from src.schedule.repositories.teacher import teacher_repos
from src.database import session_factory
from sqlalchemy import select, and_


class TeacherLoadListRepos(TeacherLoadListStore):
    async def get(id: int) -> Optional[TeacherLoadList]:
        pass

    async def get_all(self) -> List[TeacherLoadList]:
        ids = await DBUtils.select_all_id(TeacherLoadList)
        result: List[TeacherLoadList]
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: TeacherLoadList, load_list_id: int) -> IdSchema:
        teacher_id = await teacher_repos.add(obj.teacher)
        obj_db = TeacherLoadListDB(
            id=obj.id,
            load_list_id=load_list_id,
            teacher_id=teacher_id,
            hours=obj.hours
        )
        await DBUtils.insert_new(obj_db)
        async with session_factory() as session:
            query = select(TeacherLoadListDB).where(
                and_(
                    TeacherLoadListDB.hours == obj.hours,
                    TeacherLoadListDB.load_list_id == load_list_id,
                    TeacherLoadListDB.teacher_id == teacher_id
                )
            )
            query_result = await session.execute(query)
            obj_db = query_result.scalar()
        return obj_db.id

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TeacherLoadListDB, id)

    async def edit(self, obj: TeacherLoadList, load_list_id: int) -> None:
        await self.delete(obj.id)
        await self.add(obj, load_list_id=load_list_id)


teacher_load_list_repos = TeacherLoadListRepos()
