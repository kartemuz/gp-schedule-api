from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.persistence.database import (
    BaseDB,
    str_PK,
    SHORT_STRING_LENGTH,
    LONG_STRING_LENGTH
)


class OrganizationDB(BaseDB):
    __tablename__ = 'organization'
    name: Mapped[str_PK]
    address: Mapped[str] = mapped_column(String(LONG_STRING_LENGTH))
    phone: Mapped[str] = mapped_column(String(SHORT_STRING_LENGTH))
    email: Mapped[str] = mapped_column(String(SHORT_STRING_LENGTH))


class SocialNetworkDB(BaseDB):
    __tablename__ = 'social_network'
    name: Mapped[str_PK]
    value: Mapped[str] = mapped_column(
        String(LONG_STRING_LENGTH), unique=True, nullable=False)
