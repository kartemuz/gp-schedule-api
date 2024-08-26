from typing import List, Optional
from pydantic import BaseModel, EmailStr
from src.schemas import FullName


class Action(BaseModel):
    name: str


class Entity(BaseModel):
    name: str


class Opportunity(BaseModel):
    name: str
    action: Action
    entity: Entity


class Role(BaseModel):
    name: str
    opportunities: List[Opportunity]


class User(BaseModel):
    role: Optional[Role]
    login: str
    email: Optional[EmailStr]
    hashed_password: bytes
    full_name: Optional[FullName]
    active: bool


class UserEditSchema(BaseModel):
    role: Optional[Role] = None
    login: str
    email: Optional[EmailStr] = None
    hashed_password: Optional[bytes] = None
    full_name: Optional[FullName] = None
    active: Optional[None] = None
