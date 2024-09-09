from pydantic import BaseModel, EmailStr
from src.config import settings
from typing import Optional, List


class SocialNetwork(BaseModel):
    name: str
    value: str


class Organization(BaseModel):
    id: Optional[int]
    name: str
    full_name: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]

    social_networks: Optional[List[SocialNetwork]]
