from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import BaseDB, int_pk
from src.constants import DBConstants
from src.utils import DBUtils
from src.user.models import UserDB


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

    type_direction: Mapped['TypeDirectionDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )

    disciplines_directions: Mapped[List['DisciplineDirection']] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class DisciplineDirection(BaseDB):
    __tablename__ = 'discipline_direction'
    id: Mapped[int_pk]
    discipline_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(DisciplineDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False,
    )
    direction_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(DirectionDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )

    discipline: Mapped['DisciplineDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class GroupDB(BaseDB):
    __tablename__ = 'group'
    id: Mapped[int_pk]
    direction_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(DirectionDB, 'id')
        ),
        nullable=True
    )
    number_group: Mapped[int] = mapped_column(nullable=False, unique=True)

    direction: Mapped['DirectionDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class FlowDB(BaseDB):
    __tablename__ = 'flow'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False,
        unique=True
    )

    flows_groups: Mapped[List['FlowGroupDB']] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class FlowGroupDB(BaseDB):
    __tablename__ = 'flow_group'
    id: Mapped[int_pk]
    flow_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(FlowDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )
    group_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(GroupDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )

    group: Mapped['GroupDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
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
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False
    )


class LoadListDB(BaseDB):
    __tablename__ = 'load_list'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False,
        unique=True
    )
    user_login: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(UserDB, 'login'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )


class LoadDB(BaseDB):
    __tablename__ = 'load'
    id: Mapped[int_pk]
    load_list_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(LoadListDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(TeacherDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )
    hours: Mapped[int] = mapped_column(
        nullable=False
    )
