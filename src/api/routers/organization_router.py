from fastapi import APIRouter, HTTPException, status, Depends
from src.core.schemes.organization import Organization, SocialNetwork
from typing import Optional, Final, List
from src.presentation.controllers import OrganizationController
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from loguru import logger
from src.application.auth.auth_utils import JWTUtils


OGRANIZATION_TAG: Final = 'organization'

organization_router = APIRouter(
    prefix="/organization",
    tags=[OGRANIZATION_TAG]
)

http_bearer = HTTPBearer()
organization_controller = OrganizationController()


@organization_router.get('/get')
async def get_organization() -> Organization:

    try:
        result: Organization = await organization_controller.get_organization()
        return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@ organization_router.post('/edit')
async def edit_organization(obj: Organization, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    try:
        await organization_controller.edit_organization(obj)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


social_networks_router = APIRouter(
    prefix="/social_networks",
    tags=[OGRANIZATION_TAG]
)


@ social_networks_router.get('/get')
async def get_social_networks(name: Optional[str] = None) -> SocialNetwork | List[SocialNetwork]:
    try:
        result: SocialNetwork | List[SocialNetwork]
        if name is None:
            result = await organization_controller.get_all_social_networks()
        else:
            result = await organization_controller.get_social_network(name=name)
        return result
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@ social_networks_router.post('/add')
async def add_social_network(obj: SocialNetwork, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        await organization_controller.add_social_network(obj)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@ social_networks_router.get('/delete')
async def delete_social_network(name: str, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    try:
        await organization_controller.delete_social_network(name=name)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@ social_networks_router.post('/edit')
async def edit_social_network(obj: SocialNetwork, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    try:
        await organization_controller.edit_social_network(obj)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

organization_router.include_router(social_networks_router)
