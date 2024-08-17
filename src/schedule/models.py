from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import BaseDB, int_pk
from src.constants import DBConstants
from src.utils import DBUtils


class DisciplineDB(BaseDB):
    __tablename__ = 'discipline'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False,
        unique=True
    )
    lecture_hours: Mapped[int]
    practice_hours: Mapped[int]


class TypeDirectionDB(BaseDB):
    __tablename__ = 'type_direction'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        unique=True,
        nullable=False
    )


class DirectionDB(BaseDB):
    __tablename__ = 'direction'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False,
        unique=True
    )
    id_sys: Mapped[int]
    type_direction_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(TypeDirectionDB, 'id')
        ),
        nullable=False
    )
    hours: Mapped[int] = mapped_column(nullable=False)


class GroupDB(BaseDB):
    __tablename__ = 'group'
    id: Mapped[int_pk]
    direction_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(DirectionDB, 'id')
        )
    )
    number_group: Mapped[int] = mapped_column(nullable=False, unique=True)


class FlowDB(BaseDB):
    __tablename__ = 'flow'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False,
        unique=True
    )


class FlowGroupDB(BaseDB):
    __tablename__ = 'flow_group'
    id: Mapped[int_pk]
    flow_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(FlowDB, 'id')
        ),
        nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(GroupDB, 'id')
        )
    )


class TeacherDB(BaseDB):
    __tablename__ = 'teacher'
    id: Mapped[int_pk]
    surname: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False
    )
    patronymic: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False
    )
    position: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH)
    )
