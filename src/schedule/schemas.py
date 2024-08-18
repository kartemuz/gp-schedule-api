from pydantic import BaseModel
from typing import List, Optional
from src.schemas import FullName


class Discipline(BaseModel):
    id: Optional[int]
    name: str
    lecture_hours: int
    practice_hours: int


class TypeDirection(BaseModel):
    id: Optional[int]
    name: str


class Direction(BaseModel):
    id: Optional[int]
    name: str
    id_sys: int
    type_direction: TypeDirection
    hours: int
    disciplines: List[Discipline]


class Group(BaseModel):
    id: Optional[int]
    number_group: int
    direction: Direction


class Flow(BaseModel):
    id: Optional[int]
    name: str
    groups: List[Group]


class Teacher(BaseModel):
    id: Optional[int]
    full_name: Optional[FullName]
    position: Optional[str]
