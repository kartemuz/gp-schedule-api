from pydantic import BaseModel
from typing import Optional


class FullName(BaseModel):
    surname: Optional[str]
    name: Optional[str]
    patronymic: Optional[str]


class IdSchema(BaseModel):
    id: int
