from typing import Optional
from pydantic import BaseModel
from src.core.schemes.base_loggable import BaseLoggable


class FullName(BaseLoggable, BaseModel):
    surname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
