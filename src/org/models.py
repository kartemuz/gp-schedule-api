from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import BaseDB, str_pk
from src.constants import DBConstants


class OrgDB(BaseDB):
    __tablename__ = 'organization'
    name: Mapped[str_pk]
    address: Mapped[str] = mapped_column(
        String(DBConstants.SHORT_STRING_LENGTH))
    phone: Mapped[str] = mapped_column(String(DBConstants.SHORT_STRING_LENGTH))
    email: Mapped[str] = mapped_column(String(DBConstants.SHORT_STRING_LENGTH))


class SocNetDB(BaseDB):
    __tablename__ = 'social_network'
    name: Mapped[str_pk]
    value: Mapped[str] = mapped_column(
        String(DBConstants.LONG_STRING_LENGTH), unique=True, nullable=False)
