from src.schedule.stores import DirectionStore
from typing import Optional, List
from src.schedule.schemas import Direction, Discipline, TypeDirection, DirectionInput
from src.schemas import IdSchema
from src.schedule.models import DirectionDB, DisciplineDirectionDB
from sqlalchemy import select
from src.database import session_factory
from sqlalchemy.orm import selectinload
from src.utils import DBUtils

from src.schedule.repositories.discipline import discipline_repos
from src.schedule.repositories.type_direction import type_direction_repos


class DirectionRepos(DirectionStore):
    async def get_by_name(self, name: str) -> Optional[Direction]:
        async with session_factory() as session:
            query = select(DirectionDB).where(DirectionDB.name == name).options(
                selectinload(
                    DirectionDB.disciplines_directions
                ).selectinload(
                    DisciplineDirectionDB.discipline
                ),

                selectinload(DirectionDB.type_direction)
            )
            query_result = await session.execute(query)
            obj_db = query_result.scalar()
            if obj_db:
                disciplines: List[Discipline] = []
                for disc_dir in obj_db.disciplines_directions:
                    disciplines.append(
                        Discipline(
                            id=disc_dir.discipline.id,
                            name=disc_dir.discipline.name,
                            lecture_hours=disc_dir.discipline.lecture_hours,
                            practice_hours=disc_dir.discipline.practice_hours
                        )
                    )
                result = Direction(
                    id=obj_db.id,
                    name=obj_db.name,
                    id_sys=obj_db.id_sys,
                    hours=obj_db.hours,
                    type_direction=TypeDirection(
                        id=obj_db.type_direction.id,
                        name=obj_db.type_direction.name
                    ),
                    disciplines=disciplines
                )
            else:
                result = None
        return result

    async def get(self, id: int) -> Optional[Direction]:
        async with session_factory() as session:
            query = select(DirectionDB).where(DirectionDB.id == id).options(
                selectinload(
                    DirectionDB.disciplines_directions
                ).selectinload(
                    DisciplineDirectionDB.discipline
                ),

                selectinload(DirectionDB.type_direction)
            )
            query_result = await session.execute(query)
            obj_db = query_result.scalar()
            if obj_db:
                disciplines: List[Discipline] = []
                for disc_dir in obj_db.disciplines_directions:
                    disciplines.append(
                        Discipline(
                            id=disc_dir.discipline.id,
                            name=disc_dir.discipline.name,
                            lecture_hours=disc_dir.discipline.lecture_hours,
                            practice_hours=disc_dir.discipline.practice_hours
                        )
                    )
                result = Direction(
                    id=obj_db.id,
                    name=obj_db.name,
                    id_sys=obj_db.id_sys,
                    hours=obj_db.hours,
                    type_direction=TypeDirection(
                        id=obj_db.type_direction.id,
                        name=obj_db.type_direction.name
                    ),
                    disciplines=disciplines
                )
            else:
                result = None
        return result

    async def get_all(self) -> List[Direction]:
        result: List[Direction] = []
        all_id = await DBUtils.select_all_id(DirectionDB)
        for id in all_id:
            result.append(await self.get(id))
        return result

    async def add(self, obj: DirectionInput) -> IdSchema:
        # for disc in obj.disciplines:
        #     await discipline_repos.add(disc)
        # await type_direction_repos.add(obj.type_direction)
        obj_db = DirectionDB(
            id=obj.id,
            name=obj.name,
            id_sys=obj.id_sys,
            type_direction_id=obj.type_direction.id,
            hours=obj.hours
        )
        await DBUtils.insert_new(obj_db)

        async with session_factory() as session:
            query = select(DirectionDB).where(DirectionDB.name == obj.name)
            query_result = await session.execute(query)
            result = IdSchema(id=query_result.scalar().id)

        for disc in obj.disciplines:
            disc_dir_db = DisciplineDirectionDB(
                discipline_id=disc.id,
                direction_id=result
            )
            await DBUtils.insert_new(disc_dir_db)

        return result

    async def delete(self, id: int) -> None:
        await DBUtils.delete_by_id(DirectionDB, id)

    async def edit(self, obj: DirectionInput) -> None:
        await self.delete(obj.id)
        await self.add(obj)


direction_repos = DirectionRepos()
