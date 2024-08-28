from src.schedule.stores import FlowStore
from typing import Optional, List
from src.schedule.schemas import Flow, Group, FlowInput
from src.schemas import IdSchema
from src.schedule.models import FlowDB, FlowGroupDB, GroupDB
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database import session_factory
from src.utils import DBUtils
from sqlalchemy.orm import selectinload
from src.schedule.repositories.direction import direction_repos
from src.schedule.repositories.group import group_repos


class FlowRepos(FlowStore):
    async def get(self, id: int) -> Optional[Flow]:
        async with session_factory() as session:
            query = select(FlowDB).where(FlowDB.id == id).options(
                selectinload(FlowDB.flows_groups).selectinload(
                    FlowGroupDB.group
                ).selectinload(
                    GroupDB.direction
                )
            )
            query_result = await session.execute(query)
            flow_db = query_result.scalar()
            if flow_db:

                groups: List[Group] = []
                for fl_gr_db in flow_db.flows_groups:
                    groups.append(
                        Group(
                            id=fl_gr_db.group.id,
                            number_group=fl_gr_db.group.number_group,
                            direction=await direction_repos.get(id=fl_gr_db.group.direction.id)
                        )
                    )

                result = Flow(
                    id=flow_db.id,
                    name=flow_db.name,
                    groups=groups
                )

            else:
                result = None
        return result

    async def get_all(self) -> List[Flow]:
        ids: List[int] = await DBUtils.select_all_id(FlowDB)
        result = []
        for id in ids:
            result.append(await self.get(id))
        return result

    async def add(self, obj: FlowInput) -> IdSchema:
        flow_db = FlowDB(
            id=obj.id,
            name=obj.name
        )
        await DBUtils.insert_new(flow_db)

        flow_db = await DBUtils.select_by_name(FlowDB, obj.name)
        result = flow_db.id

        for gr in obj.groups:
            fl_gr_db = FlowGroupDB(
                flow_id=result,
                group_id=gr.id
            )
            await DBUtils.insert_new(fl_gr_db)

        return result

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(FlowDB, id)

    async def edit(self, obj: FlowInput) -> None:
        await self.delete(obj.id)
        await self.add(obj)


flow_repos = FlowRepos()
