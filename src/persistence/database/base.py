from src.config import settings
from typing import Tuple, Annotated, Final, Optional, List
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import select, String

engine = create_async_engine(
    url=settings.db_url,
    echo=settings.DEBUG_STATUS
)
session_factory = async_sessionmaker(engine)

SHORT_STRING_LENGTH: Final = 100
LONG_STRING_LENGTH: Final = 1000
ONDELETE_CASCADE: Final = 'CASCADE'
RELATIONSHIP_CASCADE: Final = 'all, delete-orphan'
RELATIONSHIP_LAZY_JOINED: Final = 'joined'

int_PK = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_PK = Annotated[str,  mapped_column(
    String(SHORT_STRING_LENGTH), primary_key=True)]


class BaseDB(DeclarativeBase):
    repr_cols_num = 4
    repr_cols: Tuple[str] = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), так как могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


def get_id_path(model: BaseDB) -> str:
    ID_ATTRIBUTE: Final = 'id'
    return f'{model.__tablename__}.{ID_ATTRIBUTE}'


class BaseSelect():
    @staticmethod
    async def select_by_id(model: BaseDB, id: int) -> Optional[BaseDB]:
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
    async def select_by_name(model: BaseDB, name: str) -> Optional[BaseDB]:
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
    async def select_id_by_name(model: BaseDB, name: str) -> Optional[int]:
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
            obj_db = await BaseSelect.select_by_name(model=model, name=name)
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
