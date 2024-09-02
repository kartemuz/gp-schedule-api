from pydantic import BaseModel
from typing import List, Optional
from src.schemas import FullName
from datetime import date, time
from src.schemas import IdSchema
from src.user.schemas import LoginSchema


class FreeObjectInput(BaseModel):
    time_start: time
    time_end: time
    date_: date
    schedule_list_id: int


class DirectionInput(BaseModel):
    id: Optional[int]
    name: str
    id_sys: int
    type_direction: IdSchema
    hours: int
    disciplines: List[IdSchema]


class GroupInput(BaseModel):
    id: Optional[int]
    number_group: int
    direction: IdSchema


class FlowInput(BaseModel):
    id: Optional[int]
    name: str
    groups: List[IdSchema]


class LoadListInput(BaseModel):
    id: Optional[int]
    name: str
    user: LoginSchema


class ScheduleListInput(BaseModel):
    id: Optional[int]
    name: str
    date_start: date
    date_ent: date
    active: bool
    load_list: IdSchema


class ChangeInput(BaseModel):
    id: Optional[int]
    teacher: IdSchema
    schedule_teacher: IdSchema


class TeacherLoadListInput(BaseModel):
    id: Optional[int]
    teacher: IdSchema
    load_list: IdSchema
    hours: int


class ChangeInput(BaseModel):
    id: Optional[int]
    teacher: IdSchema


class ScheduleTeacherInput(BaseModel):
    id: Optional[int]
    teacher: IdSchema
    change: Optional[ChangeInput]


class ScheduleInput(BaseModel):
    id: Optional[int]
    date_: date
    time_start: time
    time_end: time
    type_lesson: IdSchema
    flow: IdSchema
    discipline: IdSchema
    room: IdSchema
    schedule_list: IdSchema
    schedule_teacher: ScheduleTeacherInput


class Discipline(BaseModel):
    id: Optional[int]
    name: str
    lecture_hours: int
    practice_hours: int


class TypeDirection(BaseModel):
    id: Optional[int]
    name: str
    full_name: str


class Direction(BaseModel):
    id: Optional[int]
    name: str
    id_sys: str
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
    full_name: FullName
    position: str
    profile: str


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


class Change(BaseModel):
    id: Optional[int]
    teacher: Teacher


class ScheduleTeacher(BaseModel):
    id: Optional[int]
    teacher: Teacher
    change: Change


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
    schedule_teacher: ScheduleTeacher
