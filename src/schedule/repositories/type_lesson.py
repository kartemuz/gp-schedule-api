from src.schedule.stores import TypeLessonStore
from typing import Optional, List
from src.schedule.schemas import TypeLesson
from src.schemas import IdSchema
from src.schedule.models import TypeLessonDB
from src.utils import DBUtils


class TypeLessonRepos(TypeLessonStore):
    async def get(self, id: int) -> Optional[TypeLesson]:
        obj_db = await DBUtils.select_by_id(TypeLessonDB, id)
        if obj_db:
            result = TypeLesson(
                id=obj_db.id,
                name=obj_db.name
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[TypeLesson]:
        result: List[TypeLesson] = []
        objs_db: List[TypeLessonDB] = await DBUtils.select_all(TypeLessonDB)
        for obj_db in objs_db:
            result.append(
                TypeLesson(
                    id=obj_db.id,
                    name=obj_db.name
                )
            )
        return result

    async def add(self, obj: TypeLesson) -> IdSchema:
        obj_db = TypeLessonDB(
            id=obj.id,
            name=obj.name
        )
        await DBUtils.insert_new(obj_db)
        obj_db: TypeLessonDB = await DBUtils.select_by_name(TypeLessonDB, obj.name)
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TypeLessonDB, id)

    async def edit(self, obj: TypeLesson) -> None:
        obj_db = TypeLessonDB(
            id=obj.id,
            name=obj.name
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=TypeLessonDB, **data)


type_lesson_repos = TypeLessonRepos()
