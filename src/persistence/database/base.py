from src.config import settings
from typing import Tuple, Annotated, Final
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

engine = create_async_engine(
    url=settings.db_url,
    echo=settings.DEBUG_STATUS
)
session_factory = async_sessionmaker(engine)
int_PK = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

SHORT_STRING_LENGTH: Final = 30
LONG_STRING_LENGTH: Final = 1000
ONDELETE_CASCADE = 'CASCADE'
RELATIONSHIP_CASCADE = 'all, delete-orphan'


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
    ID_ATTRIBUTE: Final = 'id'
    return f'{model_db.__tablename__}.{ID_ATTRIBUTE}'
