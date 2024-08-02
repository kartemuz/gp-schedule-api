from typing import Optional, List
from pydantic import BaseModel
from src.core.schemes.base_loggable import BaseLoggable
from loguru import logger
from src.core.exceptions import EmailNotValidError
from src.core.schemes.full_name import FullName
from email_validator import validate_email


class Action(BaseLoggable, BaseModel):
    id: Optional[int] = None
    name: str


class Entity(BaseLoggable, BaseModel):
    id: Optional[int] = None
    name: str


class Opportunity(BaseLoggable, BaseModel):
    id: Optional[int] = None
    code: str
    action: Action
    entity: Entity


class Role(BaseLoggable, BaseModel):
    id: Optional[int] = None
    name: str
    opportunities: List[Opportunity] = []


class User(BaseLoggable, BaseModel):
    id: Optional[int] = None
    role: Role
    login: str
    email: str
    password: str
    full_name: FullName

    def __init__(self, email: str, login: str, id: Optional[int] = None, *args, **kwargs) -> None:

        # Check email
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as ex:
            message = 'Incorrect email'
            extra_info = {
                'id': id,
                'login': login,
                'email': email
            }
            logger.error(f'{message} {extra_info}')
            raise ex

        super().__init__(id=id, login=login, email=email, *args, **kwargs)

    # def __init__(self, role: Role, login: str, email: str, password: str, full_name: FullName, id: Optional[int] = None) -> None:

    #     # Check email
    #     try:
    #         validate_email(email, check_deliverability=False)
    #     except EmailNotValidError:
    #         message = 'Incorrect email'
    #         extra_info = {
    #             'id': id,
    #             'login': login,
    #             'email': email
    #         }
    #         logger.error(f'{message} {extra_info}')

    #     super().__init__(id=id, role=role, login=login,
    #                      email=email, password=password, full_name=full_name)
