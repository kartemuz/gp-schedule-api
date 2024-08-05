from src.core.schemes.base_loggable import BaseLoggable
from src.core.schemes.organization import Organization, SocialNetwork
from pydantic import BaseModel
from typing import List


class OrganizationResponse(BaseLoggable, BaseModel):
    status: str
    details: str
    data: Organization


class SocialNetworkResponse(BaseLoggable, BaseModel):
    status: str
    details: str
    data: SocialNetwork


class SocialNetworksListResponse(BaseLoggable, BaseModel):
    status: str
    details: str
    data: List[SocialNetwork]
