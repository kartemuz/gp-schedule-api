from typing import List, Optional
from pydantic import BaseModel, EmailStr
from src.schemas import FullName, NameSchema


class LoginSchema(BaseModel):
    login: str


class UserChangePassword(BaseModel):
    login: str
    hashed_password: str


class UserInput(BaseModel):
    role: NameSchema
    login: str
    email: EmailStr
    hashed_password: str
    full_name: FullName
    active: bool


class RoleInput(BaseModel):
    name: NameSchema
    opportunities: List[NameSchema]


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
