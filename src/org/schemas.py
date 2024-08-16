from pydantic import BaseModel, EmailStr
from src.config import settings
from typing import Optional, List


class SocialNetwork(BaseModel):
    name: str
    value: str


class Organization(BaseModel):
    name: str = settings.org.name
    address: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]

    social_networks: Optional[List[SocialNetwork]]
