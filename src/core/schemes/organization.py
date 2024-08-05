from pydantic import BaseModel
from typing import Optional, List
from src.core.schemes.base_loggable import BaseLoggable
from email_validator import validate_email
from src.core.exceptions import EmailNotValidError
from loguru import logger
from src.config import settings


class SocialNetwork(BaseLoggable, BaseModel):
    name: str
    value: str


class Organization(BaseLoggable, BaseModel):
    name: str = settings.ORGANIZATION_NAME
    address: str
    phone: str
    email: str

    social_networks: List[SocialNetwork]

    def __init__(self, email: str, *args, **kwargs) -> None:
        # Check email
        try:
            validate_email(email, check_deliverability=False)
        except EmailNotValidError as ex:
            message = 'Incorrect email'
            extra_info = {
                'email': email
            }
            logger.error(f'{message} {extra_info}')
            raise ex

        super().__init__(email=email, *args, **kwargs)
