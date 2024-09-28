from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import BaseDB, int_pk
from src.constants import DBConstants
from src.utils import DBUtils
from src.user.models import UserDB
from datetime import date, time


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

    full_name: Mapped[str] = mapped_column(
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
    id_sys: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH),
        nullable=False
    )
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

    disciplines_directions: Mapped[List['DisciplineDirectionDB']] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN,
        cascade=DBConstants.RELATIONSHIP_CASCADE
    )


class DisciplineDirectionDB(BaseDB):
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
        nullable=False
    )
    number_group: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=False, unique=True)

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
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN,
        cascade=DBConstants.RELATIONSHIP_CASCADE
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
    profile: Mapped[str] = mapped_column(
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

    teacher_load_lists: Mapped[List['TeacherLoadListDB']] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class TeacherLoadListDB(BaseDB):
    __tablename__ = 'teacher_load_list'
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

    teacher: Mapped['TeacherDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class TypeLessonDB(BaseDB):
    __tablename__ = 'type_lesson'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(DBConstants.SHORT_STRING_LENGTH),
                                      nullable=False, unique=True)


class RoomDB(BaseDB):
    __tablename__ = 'room'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(DBConstants.SHORT_STRING_LENGTH),
                                      nullable=False, unique=True)
    profile: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=False)


class ScheduleListDB(BaseDB):
    __tablename__ = 'schedule_list'
    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(DBConstants.SHORT_STRING_LENGTH),
                                      nullable=False, unique=True)
    date_start: Mapped[date] = mapped_column(nullable=False)
    date_end: Mapped[date] = mapped_column(nullable=False)
    load_list_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(LoadListDB, 'id')
        ),
        nullable=False
    )
    active: Mapped[bool] = mapped_column(nullable=False)

    load_list: Mapped['LoadListDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class ScheduleDB(BaseDB):
    __tablename__ = 'schedule'
    id: Mapped[int_pk]
    schedule_list_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(ScheduleListDB, 'id')
        )
    )
    date_: Mapped[date] = mapped_column(nullable=False)
    time_start: Mapped[time] = mapped_column(nullable=False)
    time_end: Mapped[time] = mapped_column(nullable=False)
    type_lesson_id: Mapped[int] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(TypeLessonDB, 'id'),
                   ondelete=DBConstants.ONDELETE_CASCADE),
        nullable=False
    )
    flow_id: Mapped[int] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(FlowDB, 'id'),
                   ondelete=DBConstants.ONDELETE_CASCADE),
        nullable=False
    )
    discipline_id: Mapped[int] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(DisciplineDB, 'id'),
                   ondelete=DBConstants.ONDELETE_CASCADE),
        nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(RoomDB, 'id'), ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )

    type_lesson: Mapped['TypeLessonDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )
    flow: Mapped['FlowDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )
    discipline: Mapped['DisciplineDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )
    room: Mapped['RoomDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )

    schedule_teachers: Mapped[List['ScheduleTeacherDB']] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class ScheduleTeacherDB(BaseDB):
    __tablename__ = 'schedule_teacher'
    id: Mapped[int_pk]
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(TeacherDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )
    schedule_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(ScheduleDB, 'id'),
            ondelete=DBConstants.ONDELETE_CASCADE
        ),
        nullable=False
    )

    teacher: Mapped['TeacherDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )
    change: Mapped[Optional['ChangeDB']] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class ChangeDB(BaseDB):
    __tablename__ = 'change'
    id: Mapped[int_pk]
    schedule_teacher_id: Mapped[int] = mapped_column(
        ForeignKey(
            DBUtils.get_attribute_path(ScheduleTeacherDB, 'id'),
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
    teacher: Mapped['TeacherDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )
