from src.schedule.stores import DisciplineStore
from typing import Optional, List
from src.schedule.schemas import Discipline
from src.schemas import IdSchema
from src.schedule.models import DisciplineDB
from src.utils import DBUtils


class DisciplineRepos(DisciplineStore):

    async def get(self, id: int) -> Optional[Discipline]:
        obj_db: Optional[Discipline] = await DBUtils.select_by_id(DisciplineDB, id)
        if obj_db:
            result = Discipline(
                id=obj_db.id,
                name=obj_db.name,
                lecture_hours=obj_db.lecture_hours,
                practice_hours=obj_db.practice_hours
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[Discipline]:
        result = []
        objs_db: List[Discipline] = await DBUtils.select_all(DisciplineDB)
        for obj_db in objs_db:
            result.append(
                Discipline(
                    id=obj_db.id,
                    name=obj_db.name,
                    lecture_hours=obj_db.lecture_hours,
                    practice_hours=obj_db.practice_hours
                )
            )
        return result

    async def add(self, obj: Discipline) -> IdSchema:
        obj_db = DisciplineDB(
            id=obj.id,
            name=obj.name,
            lecture_hours=obj.lecture_hours,
            practice_hours=obj.practice_hours
        )
        await DBUtils.insert_new(obj_db)

        obj_db: DisciplineDB = await DBUtils.select_by_name(DisciplineDB, obj.name)
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(DisciplineDB, id)

    async def edit(self, obj: Discipline) -> None:
        obj_db = DisciplineDB(
            id=obj.id,
            name=obj.name,
            lecture_hours=obj.lecture_hours,
            practice_hours=obj.practice_hours
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=DisciplineDB, **data)


discipline_repos = DisciplineRepos()
