from typing import Final, Optional, List
from src.persistence.database import BaseDB, session_factory
from sqlalchemy import select


class ModelPath:
    @staticmethod
    def get_name_path(model: BaseDB) -> str:
        NAME_ATTRIBUTE: Final = 'name'
        return f'{model.__tablename__}.{NAME_ATTRIBUTE}'

    @staticmethod
    def get_id_path(model: BaseDB) -> str:
        ID_ATTRIBUTE: Final = 'id'
        return f'{model.__tablename__}.{ID_ATTRIBUTE}'


class BaseQueries():
    @staticmethod
    async def select_by_id(model: BaseDB, id: int) -> BaseDB:
        result: Optional[BaseDB]
        async with session_factory() as session:
            query = select(model).where(model.id == id)
            query_result = await session.execute(query)
            if query_result is not None:
                result = query_result.scalar()
            else:
                result = None
        return result

    @staticmethod
    async def select_all_id(model: BaseDB) -> List[int]:
        result: List[int]

        async with session_factory() as session:
            query = select(model.id)
            query_result = await session.execute(query)
            result = query_result.scalars()
        return result

    @staticmethod
    async def select_all_name(model: BaseDB) -> List[str]:
        result: List[str]

        async with session_factory() as session:
            query = select(model.name)
            query_result = await session.execute(query)
            result = query_result.scalars()
        return result

    @staticmethod
    async def select_by_name(model: BaseDB, name: str) -> BaseDB:
        result: Optional[BaseDB]
        async with session_factory() as session:
            query = select(model).where(model.name == name)
            query_result = await session.execute(query)
            if query_result is not None:
                result = query_result.scalar()
            else:
                result = None
        return result

    @staticmethod
    async def select_id_by_name(model: BaseDB, name: str) -> int:
        result: Optional[int]
        async with session_factory() as session:
            query = select(model.id).where(model.name == name)
            query_result = await session.execute(query)
            if query_result is not None:
                result = query_result.scalar()
            else:
                result = None
        return result

    @staticmethod
    async def delete_by_name(model: BaseDB, name: str) -> None:
        async with session_factory() as session:
            obj_db = await BaseQueries.select_by_name(model=model, name=name)
            await session.delete(obj_db)
            await session.commit()

    @staticmethod
    async def select_all(model: BaseDB) -> List[BaseDB]:
        result: List[str]
        async with session_factory() as session:
            query = select(model)
            query_result = await session.execute(query)
            if query_result is not None:
                result = query_result.scalars()
            else:
                result = None
        return result
