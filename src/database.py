from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from src.config import settings
from typing import Annotated, Tuple
from sqlalchemy import String
from src.config import settings

engine = create_async_engine(
    url=settings.db.url,
    echo=settings.debug
)

session_factory = async_sessionmaker(engine)

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_pk = Annotated[str,  mapped_column(
    String(settings.db.short_string_length), primary_key=True)]


class BaseDB(DeclarativeBase):
    repr_cols_num = settings.db.repr_cols_num
    repr_cols: Tuple[str] = tuple()

    def __repr__(self):
        '''Relationships не используются в repr(), так как могут вести к неожиданным подгрузкам'''
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')

        return f"<{self.__class__.__name__} {', '.join(cols)}>"
