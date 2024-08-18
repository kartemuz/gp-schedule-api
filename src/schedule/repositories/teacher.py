from src.schedule.stores import TeacherStore
from typing import Optional, List
from src.schedule.schemas import Teacher
from src.schedule.models import TeacherDB
from src.schemas import FullName
from src.utils import DBUtils


class TeacherRepos(TeacherStore):
    async def get(self, id: int) -> Optional[Teacher]:
        obj_db = await DBUtils.select_by_id(TeacherDB, id)
        if obj_db:
            result = Teacher(
                id=obj_db.id,
                full_name=FullName(
                    surname=obj_db.surname,
                    name=obj_db.name,
                    patronymic=obj_db.patronymic
                ),
                position=obj_db.position
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
                    position=obj_db.position
                )
            )
        return result

    async def add(self, obj: Teacher) -> None:
        obj_db = TeacherDB(
            id=obj.id,
            surname=obj.full_name.surname,
            name=obj.full_name.name,
            patronymic=obj.full_name.patronymic,
            position=obj.position
        )
        await DBUtils.insert_new(obj_db)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TeacherDB, id)

    async def edit(self, obj: Teacher) -> None:
        await self.delete(obj.id)
        await self.add(obj)
