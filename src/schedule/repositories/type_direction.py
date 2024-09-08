from src.schedule.stores import TypeDirectionStore
from typing import Optional, List
from src.schedule.schemas import TypeDirection
from src.schemas import IdSchema
from src.schedule.models import TypeDirectionDB
from src.utils import DBUtils


class TypeDirectionRepos(TypeDirectionStore):
    async def get(self, id: int) -> Optional[TypeDirection]:
        obj_db: Optional[TypeDirectionDB] = await DBUtils.select_by_id(TypeDirectionDB, id)
        if obj_db:
            result = TypeDirection(
                id=obj_db.id,
                name=obj_db.name,
                full_name=obj_db.full_name
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[TypeDirection]:
        result: List[TypeDirection] = []
        objs_db: List[TypeDirectionDB] = await DBUtils.select_all(TypeDirectionDB)
        for obj_db in objs_db:
            result.append(
                TypeDirection(
                    id=obj_db.id,
                    name=obj_db.name,
                    full_name=obj_db.full_name
                )
            )
        return result

    async def add(self, obj: TypeDirection) -> IdSchema:
        obj_db = TypeDirectionDB(
            id=obj.id,
            name=obj.name,
            full_name=obj.full_name
        )
        await DBUtils.insert_new(obj_db)
        obj_db: TypeDirectionDB = await DBUtils.select_by_name(TypeDirectionDB, obj.name)
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TypeDirectionDB, id)

    async def edit(self, obj: TypeDirection) -> None:
        obj_db = TypeDirectionDB(
            id=obj.id,
            name=obj.name,
            full_name=obj.full_name
        )
        data = obj_db.__dict__.copy()
        data.pop('_sa_instance_state')
        await DBUtils.update_by_id(model=TypeDirectionDB, **data)


type_direction_repos = TypeDirectionRepos()
