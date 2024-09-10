from src.schedule.schemas import LoadList, TeacherLoadList, Teacher, LoadListInput
from typing import Optional, List
from src.schedule.stores import LoadListStore
from src.schemas import IdSchema
from src.schedule.models import LoadListDB, TeacherLoadListDB
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database import session_factory
from src.utils import DBUtils
from src.schemas import FullName
from src.schedule.repositories.teacher import teacher_repos


class LoadListRepos(LoadListStore):
    async def get(self, id: int) -> Optional[LoadList]:
        async with session_factory() as session:
            query = select(LoadListDB).where(
                LoadListDB.id == id
            ).options(
                selectinload(
                    LoadListDB.teacher_load_lists
                ).selectinload(
                    TeacherLoadListDB.teacher
                )
            )
            query_result = await session.execute(query)
            load_list_db = query_result.scalar()
            if load_list_db:
                teacher_load_lists = []
                for t_l in load_list_db.teacher_load_lists:
                    teacher_load_lists.append(
                        TeacherLoadList(
                            id=t_l.id,
                            hours=t_l.hours,
                            teacher=await teacher_repos.get(t_l.teacher.id)
                        )
                    )
                result = LoadList(
                    id=load_list_db.id,
                    name=load_list_db.name,
                    user_login=load_list_db.user_login,
                    teacher_load_lists=teacher_load_lists
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[LoadList]:
        ids: List[int] = await DBUtils.select_all_id(LoadListDB)
        result: List[LoadList] = []
        for id in ids:
            result.append(
                await self.get(id)
            )
        return result

    async def add(self, obj: LoadListInput) -> IdSchema:
        obj_db = LoadListDB(
            id=obj.id,
            name=obj.name,
            user_login=obj.user.login
        )
        await DBUtils.insert_new(obj_db)
        obj_db: LoadListDB = await DBUtils.select_by_name(LoadListDB, obj.name)
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(LoadListDB, id)

    async def edit(self, obj: LoadListInput) -> None:
        obj_db = LoadListDB(
            id=obj.id,
            name=obj.name,
            user_login=obj.user_login
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=LoadListDB, **data)


load_list_repos = LoadListRepos()
