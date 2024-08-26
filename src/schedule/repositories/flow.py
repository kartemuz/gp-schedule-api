from src.schedule.stores import FlowStore
from typing import Optional, List
from src.schedule.schemas import Flow, Group
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
            if query_result:
                flow_db = query_result.scalar()

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
        ids: List[int] = await DBUtils.select_all_id()
        result = []
        for id in ids:
            result.append(await self.get(id))
        return result

    async def add(self, obj: Flow) -> IdSchema:
        flow_db = FlowDB(
            id=obj.id,
            name=obj.name
        )
        await DBUtils.insert_new(flow_db)

        for gr in obj.groups:
            await group_repos.add(gr)

        flow_db = await DBUtils.select_by_name(FlowDB, obj.name)
        flow_id = flow_db.id

        async with session_factory() as session:
            for gr in obj.groups:
                query = select(GroupDB).where(
                    GroupDB.number_group == gr.number_group
                )
                query_result = await session.execute(query)
                gr_db = query_result.scalar()

                fl_gr_db = FlowGroupDB(
                    flow_id=flow_id,
                    group_id=gr_db.id
                )
                session.add(fl_gr_db)
                try:
                    await session.commit()
                except IntegrityError:
                    await session.rollback()

        return flow_id

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(FlowDB, id)

    async def edit(self, obj: Flow) -> None:
        await self.delete(obj.id)
        await self.add(obj)


flow_repos = FlowRepos()
