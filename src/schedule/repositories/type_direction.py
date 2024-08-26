from src.schedule.stores import TypeDirectionStore
from typing import Optional, List
from src.schedule.schemas import TypeDirection
from src.schemas import IdSchema
from src.schedule.models import TypeDirectionDB
from src.utils import DBUtils


class TypeDirectionRepos(TypeDirectionStore):
    async def get(self, id: int) -> Optional[TypeDirection]:
        obj_db = await DBUtils.select_by_id(TypeDirectionDB, id)
        if obj_db:
            result = TypeDirection(
                id=obj_db.id,
                name=obj_db.name
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[TypeDirection]:
        result: List[TypeDirection] = []
        objs_db = await DBUtils.select_all(TypeDirectionDB)
        for obj_db in objs_db:
            result.append(
                TypeDirection(
                    id=obj_db.id,
                    name=obj_db.name
                )
            )
        return result

    async def add(self, obj: TypeDirection) -> IdSchema:
        obj_db = TypeDirectionDB(
            id=obj.id,
            name=obj.name,
        )
        await DBUtils.insert_new(obj_db)
        obj_db: TypeDirectionDB = await DBUtils.select_by_name(TypeDirectionDB, obj.name)
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(TypeDirectionDB, id)

    async def edit(self, obj: TypeDirection) -> None:
        await self.delete(obj.id)
        await self.add(obj)


type_direction_repos = TypeDirectionRepos()
