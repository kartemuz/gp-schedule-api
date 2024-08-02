from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.persistence.database.base import (
    BaseDB,
    int_PK,
    get_id_path,
    STRING_LENGTH,
    ONDELETE_CASCADE,
    RELATIONSHIP_CASCADE
)
from loguru import logger


class ActionDB(BaseDB):
    __tablename__ = 'action'
    id: Mapped[int_PK]
    name: Mapped[str] = mapped_column(
        String(STRING_LENGTH), nullable=False, unique=True
    )

    opportunities: Mapped[List['OpportunityDB']] = relationship(
        cascade=RELATIONSHIP_CASCADE
    )


class EntityDB(BaseDB):
    __tablename__ = 'entity'
    id: Mapped[int_PK]
    name: Mapped[str] = mapped_column(
        String(STRING_LENGTH), nullable=False, unique=True
    )

    opportunities: Mapped[List['OpportunityDB']] = relationship(
        cascade=RELATIONSHIP_CASCADE
    )


class OpportunityDB(BaseDB):
    __tablename__ = 'opportunity'
    id: Mapped[int_PK]
    code: Mapped[str] = mapped_column(
        String(STRING_LENGTH), nullable=False, unique=True
    )
    action_id: Mapped[int] = mapped_column(
        ForeignKey(get_id_path(ActionDB), ondelete=ONDELETE_CASCADE)
    )
    entity_id: Mapped[int] = mapped_column(
        ForeignKey(get_id_path(EntityDB), ondelete=ONDELETE_CASCADE)
    )

    action: Mapped['ActionDB'] = relationship()
    entity: Mapped['EntityDB'] = relationship()

    role_opportunities: Mapped[List['RoleOpportunityDB']] = relationship(
        cascade=RELATIONSHIP_CASCADE
    )


class RoleDB(BaseDB):
    __tablename__ = 'role'
    id: Mapped[int_PK]
    name: Mapped[str] = mapped_column(
        String(STRING_LENGTH), nullable=False, unique=True
    )

    role_opportunities: Mapped[List['RoleOpportunityDB']] = relationship(
        cascade=RELATIONSHIP_CASCADE
    )


class RoleOpportunityDB(BaseDB):
    __tablename__ = 'role_opportunity'
    id: Mapped[int_PK]
    role_id: Mapped[int] = mapped_column(
        ForeignKey(get_id_path(RoleDB), ondelete=ONDELETE_CASCADE), nullable=False
    )
    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey(get_id_path(OpportunityDB), ondelete=ONDELETE_CASCADE), nullable=False
    )

    role: Mapped['RoleDB'] = relationship()
    opportunity: Mapped['OpportunityDB'] = relationship()


class UserDB(BaseDB):
    __tablename__ = 'user'
    id: Mapped[int_PK]
    login: Mapped[str] = mapped_column(String(STRING_LENGTH), nullable=False)
    email: Mapped[str] = mapped_column(String(STRING_LENGTH), nullable=False)
    password: Mapped[str] = mapped_column(
        String(STRING_LENGTH), nullable=False
    )
    surname: Mapped[str] = mapped_column(String(STRING_LENGTH))
    name: Mapped[str] = mapped_column(String(STRING_LENGTH))
    patronymic: Mapped[str] = mapped_column(String(STRING_LENGTH))
    role_id: Mapped[int] = mapped_column(
        ForeignKey(get_id_path(RoleDB), ondelete=ONDELETE_CASCADE), nullable=False
    )

    role: Mapped['RoleDB'] = relationship()
