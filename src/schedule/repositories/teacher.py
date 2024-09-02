from src.schedule.stores import TeacherStore
from typing import Optional, List
from src.schedule.schemas import Teacher
from src.schemas import IdSchema
from src.schedule.models import TeacherDB
from src.schemas import FullName
from src.utils import DBUtils
from src.database import session_factory
from sqlalchemy import select, and_


class TeacherRepos(TeacherStore):
    async def get(self, id: int) -> Optional[Teacher]:
        obj_db: Optional[TeacherDB] = await DBUtils.select_by_id(TeacherDB, id)
        if obj_db:
            result = Teacher(
                id=obj_db.id,
                full_name=FullName(
                    surname=obj_db.surname,
                    name=obj_db.name,
                    patronymic=obj_db.patronymic
                ),
                position=obj_db.position,
                profile=obj_db.profile
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[Teacher]:
        result: List[Teacher] = []
        objs_db: List[TeacherDB] = await DBUtils.select_all(TeacherDB)
        for obj_db in objs_db:
            result.append(
                Teacher(
                    id=obj_db.id,
                    full_name=FullName(
                        surname=obj_db.surname,
                        name=obj_db.name,
                        patronymic=obj_db.patronymic
                    ),
                    position=obj_db.position,
                    profile=obj_db.profile
                )
            )
        return result

    async def add(self, obj: Teacher) -> IdSchema:
        obj_db = TeacherDB(
            id=obj.id,
            surname=obj.full_name.surname,
            name=obj.full_name.name,
            patronymic=obj.full_name.patronymic,
            position=obj.position,
            profile=obj.profile
        )
        await DBUtils.insert_new(obj_db)
        async with session_factory() as session:
            query = select(TeacherDB).where(
                and_(
                    TeacherDB.surname == obj.full_name.surname,
                    TeacherDB.name == obj.full_name.name,
                    TeacherDB.patronymic == obj.full_name.patronymic,
                    TeacherDB.position == obj.position,
                    TeacherDB.profile == obj.profile
                )
            )
            query_result = await session.execute(query)
            obj_db = query_result.scalar()
            return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TeacherDB, id)

    async def edit(self, obj: Teacher) -> None:
        await self.delete(obj.id)
        await self.add(obj)


teacher_repos = TeacherRepos()
