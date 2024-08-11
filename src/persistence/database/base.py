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
