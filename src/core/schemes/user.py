from typing import List, Optional
from pydantic import BaseModel, EmailStr
from src.core.schemes.base_loggable import BaseLoggable
from src.core.schemes.full_name import FullName


class Action(BaseLoggable, BaseModel):
    name: str


class Entity(BaseLoggable, BaseModel):
    name: str


class Opportunity(BaseLoggable, BaseModel):
    name: str
    action: Action
    entity: Entity


class Role(BaseLoggable, BaseModel):
    name: str
    opportunities: List[Opportunity] = []


class User(BaseLoggable, BaseModel):
    role: Optional[Role] = None
    login: str
    email: EmailStr
    hashed_password: bytes
    full_name: FullName
    active: bool
    admin: bool
