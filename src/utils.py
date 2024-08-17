from src.database import BaseDB, session_factory
from typing import List, Optional
from sqlalchemy import select


class DBUtils:
    @staticmethod
    def get_attribute_path(model: BaseDB, attributte: str) -> str:
        '''Helps in connection with foreign keys'''
        return f'{model.__tablename__}.{attributte}'

    @staticmethod
    async def select_all(model: BaseDB) -> List[BaseDB]:
        async with session_factory() as session:
            query = select(model)
            query_result = await session.execute(query)
            return query_result.scalars()

    @staticmethod
    async def select_by_name(model: BaseDB, name: str) -> Optional[BaseDB]:
        async with session_factory() as session:
            query = select(model).where(model.name == name)
            query_result = await session.execute(query)
            if query_result:
                result = query_result.scalar()
            else:
                result = None
            return result

    @staticmethod
    async def select_by_name(model: BaseDB, name: str) -> Optional[BaseDB]:
        async with session_factory() as session:
            query = select(model).where(model.name == name)
            query_result = await session.execute(query)
            if query_result:
                result = query_result.scalar()
            else:
                result = None
        return result

    @staticmethod
    async def select_all_name(model: BaseDB) -> List[str]:
        async with session_factory() as session:
            query = select(model.name)
            query_result = await session.execute(query)
            return query_result.scalars()
