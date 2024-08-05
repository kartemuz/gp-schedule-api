from fastapi import APIRouter, HTTPException
from src.core.schemes.organization import Organization, SocialNetwork
from typing import List, Optional, Final
from src.services import OrganizationService
from src.persistence.repositories.organization_repositories import OrganizationRepository, SocialNetworkRepository
from src.api.responses import organization_responses, BaseResponse, STATUS_OK, NO_DETAILS
from src.api.exceptions import InternalStatusCodes
from loguru import logger


TAG: Final = 'organization'

organization_router = APIRouter(
    prefix="/organization",
    tags=[TAG]
)
service = OrganizationService(
    social_network_repository=SocialNetworkRepository,
    organization_reposotory=OrganizationRepository
)


@organization_router.get('/get')
async def get_organization() -> organization_responses.OrganizationResponse:
    try:
        data = await service.get_organization()
        return organization_responses.OrganizationResponse(
            status=STATUS_OK, details=NO_DETAILS, data=data)
    except Exception:
        raise HTTPException(status_code=InternalStatusCodes.BASE)


@ organization_router.post('/edit')
async def edit_organization(obj: Organization) -> BaseResponse:
    try:
        await service.edit_organization(obj)
        return BaseResponse(status=STATUS_OK, details=NO_DETAILS)
    except Exception:
        raise HTTPException(status_code=InternalStatusCodes.BASE)


social_networks_router = APIRouter(
    prefix="/social_networks",
    tags=[TAG]
)


@ social_networks_router.get('/get')
async def get_social_networks(name: Optional[str] = None) -> organization_responses.SocialNetworkResponse | organization_responses.SocialNetworksListResponse:
    try:
        result: organization_responses.SocialNetworkResponse | organization_responses.SocialNetworkResponse
        if name is None:
            data = await service.get_all_social_networks()
            result = organization_responses.SocialNetworksListResponse(
                status=STATUS_OK, data=data, details=NO_DETAILS)
        else:
            data = await service.get_social_network(name=name)
            result = organization_responses.SocialNetworkResponse(
                status=STATUS_OK, data=data, details=NO_DETAILS)
        return result
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=InternalStatusCodes.BASE)


@ social_networks_router.post('/add')
async def add_social_network(obj: SocialNetwork) -> BaseResponse:
    try:
        await service.add_social_network(obj)
        return BaseResponse(status=STATUS_OK, details=NO_DETAILS)
    except Exception:
        raise HTTPException(status_code=InternalStatusCodes.BASE)


@ social_networks_router.get('/delete')
async def delete_social_network(name: str) -> BaseResponse:
    try:
        await service.delete_social_network(name=name)
        return BaseResponse(status=STATUS_OK, details=NO_DETAILS)
    except Exception:
        raise HTTPException(status_code=InternalStatusCodes.BASE)


@ social_networks_router.post('/edit')
async def edit_social_network(obj: SocialNetwork) -> BaseResponse:
    try:
        await service.edit_social_network(obj)
        return BaseResponse(status=STATUS_OK, details=NO_DETAILS)
    except Exception:
        raise HTTPException(status_code=InternalStatusCodes.BASE)

organization_router.include_router(social_networks_router)
