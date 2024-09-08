from src.database import BaseDB, session_factory
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile
from src.config import settings
import os
from pathlib import Path


class FileUtils:
    @staticmethod
    async def create_dir(dir_path: str) -> None:
        if not os.path.exists(dir_path):
            os.mkdir(settings.static.dir_path)

    @staticmethod
    async def save_file(file: UploadFile) -> Path:
        file_path = os.path.join(
            settings.static.dir_path,
            file.filename
        )
        with open(file_path, 'wb') as f:
            f.write(await file.read())
        return Path(file_path)


class DBUtils:
    @staticmethod
    async def select_id_by_name(model: BaseDB, name: str) -> Optional[int]:
        async with session_factory() as session:
            query = select(model.id).where(model.name == name)
            query_result = await session.execute(query)
            return query_result.scalar()

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

    @staticmethod
    async def select_by_id(model: BaseDB, id: int) -> Optional[BaseDB]:
        async with session_factory() as session:
            return await session.get(model, id)

    @staticmethod
    async def delete_by_id(model: BaseDB, id: int) -> None:
        obj_db = await DBUtils.select_by_id(model, id)
        async with session_factory() as session:
            obj_db = await session.get(model, id)
            await session.delete(obj_db)
            await session.commit()

    @staticmethod
    async def delete_by_name(model: BaseDB, name: str) -> None:
        obj_db = await DBUtils.select_by_name(model, name)
        async with session_factory() as session:
            await session.delete(obj_db)
            await session.commit()

    @staticmethod
    async def insert_new(model_db: BaseDB) -> None:
        async with session_factory() as session:
            session.add(model_db)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    @staticmethod
    async def select_all_id(model: BaseDB) -> List[int]:
        async with session_factory() as session:
            query = select(model.id)
            query_result = await session.execute(query)
            return query_result.scalars()
