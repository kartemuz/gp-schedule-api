from pydantic import BaseModel, EmailStr
from typing import List
from src.core.schemes.base_loggable import BaseLoggable
from src.config import settings


class SocialNetwork(BaseLoggable, BaseModel):
    name: str
    value: str


class Organization(BaseLoggable, BaseModel):
    name: str = settings.ORGANIZATION_NAME
    address: str
    phone: str
    email: EmailStr

    social_networks: List[SocialNetwork]
