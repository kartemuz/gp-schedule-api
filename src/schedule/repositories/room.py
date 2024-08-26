from src.schedule.stores import RoomStore
from typing import Optional, List
from src.schedule.schemas import Room
from src.schemas import IdSchema
from src.schedule.models import RoomDB
from src.utils import DBUtils


class RoomRepos(RoomStore):
    async def get(self, id: int) -> Optional[Room]:
        obj_db = await DBUtils.select_by_id(RoomDB, id)
        if obj_db:
            result = Room(
                id=obj_db.id,
                name=obj_db.name
            )
        else:
            result = None
        return result

    async def get_all(self) -> List[Room]:
        result: List[Room] = []
        objs_db: List[RoomDB] = await DBUtils.select_all(RoomDB)
        for obj_db in objs_db:
            result.append(
                Room(
                    id=obj_db.id,
                    name=obj_db.name
                )
            )
        return result

    async def add(self, obj: Room) -> IdSchema:
        obj_db = RoomDB(
            id=obj.id,
            name=obj.name
        )
        await DBUtils.insert_new(obj_db)
        obj_db: RoomDB = await DBUtils.select_by_name(RoomDB, obj.name)
        return IdSchema(id=obj_db.id)

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(RoomDB, id)

    async def edit(self, obj: Room) -> None:
        await self.delete(obj.id)
        await self.add(obj)


room_repos = RoomRepos()
