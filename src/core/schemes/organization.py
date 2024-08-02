from pydantic import BaseModel
from typing import Optional, List
from src.core.schemes.base_loggable import BaseLoggable


class SocialNetwork(BaseLoggable, BaseModel):
    id: Optional[int] = None
    name: str
    value: str


class Organization(BaseLoggable, BaseModel):
    id: Optional[int] = None
    address: str
    phone: str
    email: str

    social_networks: List[SocialNetwork] = []
