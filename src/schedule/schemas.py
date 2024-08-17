from pydantic import BaseModel
from typing import List, Optional
from src.schemas import FullName


class Discipline(BaseModel):
    id: int
    name: str
    lecture_hours: int
    practice_hours: int


class TypeDirection(BaseModel):
    id: int
    name: str


class Direction(BaseModel):
    id: int
    name: str
    id_sys: int
    type_direction: TypeDirection
    hours: int
    disciplines: List[Discipline]


class Group(BaseModel):
    id: int
    number_group: int
    direction: Direction


class Flow(BaseModel):
    id: int
    name: str
    groups: List[Group]


class Teacher(BaseModel):
    id: int
    full_name: FullName
    position: Optional[str]
