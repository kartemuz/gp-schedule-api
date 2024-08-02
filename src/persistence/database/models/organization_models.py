from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.persistence.database.base import (
    BaseDB,
    int_PK,
    get_id_path,
    SHORT_STRING_LENGTH,
    LONG_STRING_LENGTH
)


class OrganizationDB(BaseDB):
    __tablename__ = 'organization'
    id: Mapped[int_PK]
    address: Mapped[str] = mapped_column(String(LONG_STRING_LENGTH))
    phone: Mapped[str] = mapped_column(String(SHORT_STRING_LENGTH))
    email: Mapped[str] = mapped_column(String(SHORT_STRING_LENGTH))

    social_networks: Mapped[List['SocialNetworkDB']] = relationship()


class SocialNetworkDB(BaseDB):
    __tablename__ = 'social_network'
    id: Mapped[int_PK]
    organization_id: Mapped[int] = mapped_column(
        ForeignKey(get_id_path(OrganizationDB)), nullable=False
    )
    name: Mapped[str] = mapped_column(String(SHORT_STRING_LENGTH))
    value: Mapped[str] = mapped_column(String(LONG_STRING_LENGTH))

    organization: Mapped[str] = relationship()
