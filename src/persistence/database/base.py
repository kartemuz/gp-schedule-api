from src.config import settings
from typing import Tuple, Annotated
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

# engine = create_async_engine(
#     url=settings.db_url,
#     echo=settings.DEBUG_STATUS
# )
engine = create_async_engine(
    "mysql+aiomysql://user:pass@hostname/dbname?charset=utf8mb4")
session_factory = async_sessionmaker(engine)
int_PK = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
ID_ATTRIBUTE = 'id'


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


def get_id_path(model_db: BaseDB) -> str:
    return f'{model_db.__tablename__}.id'
