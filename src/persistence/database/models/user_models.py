from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.persistence.database import (
    BaseDB,
    SHORT_STRING_LENGTH,
    ONDELETE_CASCADE,
    LONG_STRING_LENGTH,
    RELATIONSHIP_CASCADE,
    str_PK,
    int_PK,
)
from src.persistence.database.database_utils import BaseQueries, ModelPath


class ActionDB(BaseDB):
    __tablename__ = 'action'
    name: Mapped[str_PK]

    # opportunities: Mapped[List['OpportunityDB']] = relationship(
    #     cascade=RELATIONSHIP_CASCADE
    # )


class EntityDB(BaseDB):
    __tablename__ = 'entity'
    name: Mapped[str_PK]

    # opportunities: Mapped[List['OpportunityDB']] = relationship(
    #     cascade=RELATIONSHIP_CASCADE
    # )


class OpportunityDB(BaseDB):
    __tablename__ = 'opportunity'
    name: Mapped[str_PK]
    action_name: Mapped[str] = mapped_column(
        ForeignKey(ModelPath.get_name_path(ActionDB), ondelete=ONDELETE_CASCADE), nullable=False
    )
    entity_name: Mapped[str] = mapped_column(
        ForeignKey(ModelPath.get_name_path(EntityDB), ondelete=ONDELETE_CASCADE), nullable=False
    )

    action: Mapped['ActionDB'] = relationship(lazy='selectin')
    entity: Mapped['EntityDB'] = relationship(lazy='selectin')

    # role_opportunities: Mapped[List['RoleOpportunityDB']] = relationship(
    #     cascade=RELATIONSHIP_CASCADE
    # )


class RoleDB(BaseDB):
    __tablename__ = 'role'
    name: Mapped[str_PK]

    role_opportunities: Mapped[List['RoleOpportunityDB']] = relationship(
        cascade=RELATIONSHIP_CASCADE, lazy='selectin'
    )


class RoleOpportunityDB(BaseDB):
    __tablename__ = 'role_opportunity'
    id: Mapped[int_PK]
    role_name: Mapped[str] = mapped_column(
        ForeignKey(ModelPath.get_name_path(RoleDB), ondelete=ONDELETE_CASCADE), nullable=False
    )
    opportunity_name: Mapped[str] = mapped_column(
        ForeignKey(ModelPath.get_name_path(OpportunityDB), ondelete=ONDELETE_CASCADE), nullable=False
    )

    # role: Mapped['RoleDB'] = relationship()
    opportunity: Mapped['OpportunityDB'] = relationship(lazy='selectin')


class UserDB(BaseDB):
    __tablename__ = 'user'
    login: Mapped[str_PK]
    email: Mapped[str] = mapped_column(
        String(SHORT_STRING_LENGTH), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(LONG_STRING_LENGTH), nullable=False
    )
    active: Mapped[bool] = mapped_column(nullable=False, default=True)
    admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    surname: Mapped[str] = mapped_column(
        String(SHORT_STRING_LENGTH), nullable=True)
    name: Mapped[str] = mapped_column(
        String(SHORT_STRING_LENGTH), nullable=True)
    patronymic: Mapped[str] = mapped_column(
        String(SHORT_STRING_LENGTH), nullable=True)
    role_name: Mapped[str] = mapped_column(
        ForeignKey(ModelPath.get_name_path(RoleDB), ondelete=ONDELETE_CASCADE), nullable=True
    )

    role: Mapped['RoleDB'] = relationship(lazy='selectin')
