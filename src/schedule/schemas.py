from pydantic import BaseModel
from typing import List, Optional
from src.schemas import FullName
from datetime import date, time


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


class Room(BaseModel):
    id: Optional[int]
    name: str


class TypeLesson(BaseModel):
    id: Optional[int]
    name: str


class TeacherLoadList(BaseModel):
    id: Optional[int]
    teacher: Teacher
    hours: int


class LoadList(BaseModel):
    id: Optional[int]
    name: str
    user_login: str
    teacher_load_lists: List[TeacherLoadList]


class ScheduleList(BaseModel):
    id: Optional[int]
    name: str
    date_start: date
    date_end: date
    active: bool
    load_list: LoadList


class Schedule(BaseModel):
    id: Optional[int]
    date_: date
    time_start: time
    time_end: time
    type_lesson: TypeLesson
    flow: Flow
    discipline: Discipline
    room: Room

    schedule_list: ScheduleList


class ScheduleTeacher(BaseModel):
    id: Optional[int]
    teacher: Teacher
    schedule: Schedule


class Change(BaseModel):
    id: Optional[int]
    schedule_teacher: ScheduleTeacher
    teacher: Teacher
