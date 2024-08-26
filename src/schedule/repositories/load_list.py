from src.schedule.schemas import LoadList, TeacherLoadList, Teacher
from typing import Optional, List
from src.schedule.stores import LoadListStore
from src.schemas import IdSchema
from src.schedule.models import LoadListDB, TeacherLoadListDB
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database import session_factory
from src.utils import DBUtils
from src.schemas import FullName
from src.schedule.repositories.teacher_load_list import teacher_load_list_repos


class LoadListRepos(LoadListStore):
    async def get(id: int) -> Optional[LoadList]:
        async with session_factory() as session:
            query = select(LoadListDB).where(
                selectinload(
                    LoadListDB.teacher_load_lists
                ).selectinload(
                    TeacherLoadListDB.teacher
                )
            )
            query_result = await session.execute(query)
            if query_result:
                load_list_db = query_result.scalar()
                teacher_load_lists = []
                for t_l in load_list_db.teacher_load_lists:
                    teacher_load_lists.append(
                        TeacherLoadList(
                            id=t_l.id,
                            hours=t_l.hours,
                            teacher=Teacher(
                                id=t_l.teacher.id,
                                full_name=FullName(
                                    name=t_l.teacher.name,
                                    surname=t_l.teacher.surname,
                                    patronymic=t_l.teacher.patronymic
                                ),
                                position=t_l.teacher.position
                            )
                        )
                    )
                result = LoadList(
                    id=load_list_db.id,
                    name=load_list_db.name,
                    user_login=load_list_db.user_login
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[LoadList]:
        ids = await DBUtils.select_all_id(LoadListDB)
        result: List[LoadList]
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: LoadList) -> IdSchema:
        obj_db = LoadListDB(
            id=obj.id,
            name=obj.name,
            user_login=obj.user_login
        )
        await DBUtils.insert_new(obj_db)
        obj_db: LoadListDB = await DBUtils.select_by_name(LoadListDB, obj.name)
        for t_l in obj.teacher_load_lists:
            await teacher_load_list_repos.add(
                obj=t_l,
                load_list_id=obj_db.id
            )
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(LoadListDB, id)

    async def edit(self, obj: LoadList) -> None:
        await self.delete(obj.id)
        await self.add(obj)
