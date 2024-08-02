from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.persistence.database.base import BaseDB, int_PK, get_id_path


class ActionDB(BaseDB):
    __tablename__ = 'action'
    id: Mapped[int_PK]
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class EntityDB(BaseDB):
    __tablename__ = 'entity'
    id: Mapped[int_PK]
    name: Mapped[str] = mapped_column(nullable=False, unique=True)


class OpportunityDB(BaseDB):
    __tablename__ = 'opportunity'
    id: Mapped[int_PK]
    code: Mapped[str] = mapped_column(nullable=False, unique=True)
    action_id: Mapped[int] = mapped_column(ForeignKey(
        get_id_path(ActionDB), ondelete="CASCADE"))
    entity_id: Mapped[int] = mapped_column(ForeignKey(
        get_id_path(EntityDB), ondelete="CASCADE"))

    action: Mapped['ActionDB'] = relationship()
    entity: Mapped['EntityDB'] = relationship()


class RoleDB(BaseDB):
    __tablename__ = 'role'
    id: Mapped[int_PK]
    name: Mapped[str]

    role_opportunities: Mapped[List['RoleOpportunityDB']] = relationship()


class RoleOpportunityDB(BaseDB):
    __tablename__ = 'role_opportunity'
    id: Mapped[int_PK]
    role_id: Mapped[int] = mapped_column(ForeignKey(
        get_id_path(RoleDB), ondelete="CASCADE"))
    opportunity_id: Mapped[int] = mapped_column(ForeignKey(
        get_id_path(OpportunityDB), ondelete="CASCADE"))

    role: Mapped['RoleDB'] = relationship()
    opportunity: Mapped['OpportunityDB'] = relationship()


class UserDB(BaseDB):
    __tablename__ = 'user'
    id: Mapped[int_PK]
    login: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    surname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str]
    role_id: Mapped[int] = mapped_column(ForeignKey(
        get_id_path(RoleDB), ondelete="CASCADE"))

    role: Mapped['RoleDB'] = relationship()
