from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import BaseDB, str_pk, int_pk
from src.constants import DBConstants
from src.utils import DBUtils


class ActionDB(BaseDB):
    __tablename__ = 'action'
    name: Mapped[str_pk]


class EntityDB(BaseDB):
    __tablename__ = 'entity'
    name: Mapped[str_pk]


class OpportunityDB(BaseDB):
    __tablename__ = 'opportunity'
    name: Mapped[str_pk]
    action_name: Mapped[str] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(ActionDB, 'name'), ondelete=DBConstants.ONDELETE_CASCADE), nullable=False
    )
    entity_name: Mapped[str] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(EntityDB, 'name'), ondelete=DBConstants.ONDELETE_CASCADE), nullable=False
    )

    action: Mapped['ActionDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN)
    entity: Mapped['EntityDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN)


class RoleDB(BaseDB):
    __tablename__ = 'role'
    name: Mapped[str_pk]

    role_opportunities: Mapped[List['RoleOpportunityDB']] = relationship(
        cascade=DBConstants.RELATIONSHIP_CASCADE, lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN
    )


class RoleOpportunityDB(BaseDB):
    __tablename__ = 'role_opportunity'
    id: Mapped[int_pk]
    role_name: Mapped[str] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(RoleDB, 'name'), ondelete=DBConstants.ONDELETE_CASCADE), nullable=False
    )
    opportunity_name: Mapped[str] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(OpportunityDB, 'name'), ondelete=DBConstants.ONDELETE_CASCADE), nullable=False
    )

    opportunity: Mapped['OpportunityDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN)


class UserDB(BaseDB):
    __tablename__ = 'user'
    login: Mapped[str_pk]
    email: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=False
    )
    active: Mapped[bool] = mapped_column(nullable=False, default=True)
    surname: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=True)
    name: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=True)
    patronymic: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH), nullable=True)
    role_name: Mapped[str] = mapped_column(
        ForeignKey(DBUtils.get_attribute_path(RoleDB, 'name'), ondelete=DBConstants.ONDELETE_CASCADE), nullable=True
    )

    role: Mapped['RoleDB'] = relationship(
        lazy=DBConstants.RELATIONSHIP_LAZY_SELECTIN)
