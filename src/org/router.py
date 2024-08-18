from fastapi import APIRouter, Depends, HTTPException, status
from typing import Final
from src.auth.dependencies import get_auth_active_user
from src.user.schemas import User
from src.org.schemas import Organization, SocialNetwork
from src.org.service import org_service
from typing import Optional, List

tags: Final = ['organization']


org_router = APIRouter(
    prefix='/organization',
    tags=tags
)


@org_router.get('/get')
async def get_organization() -> Organization:
    return await org_service.org_store.get()


@org_router.post('/add')
async def add_organization(organization: Organization, auth_user: User = Depends(get_auth_active_user)) -> None:
    await org_service.org_store.add(organization)


@org_router.post('/edit')
async def edit_organization(organization: Organization, auth_user: User = Depends(get_auth_active_user)) -> None:
    await org_service.org_store.edit(organization)


soc_net_router = APIRouter(
    prefix='/social_network',
    tags=tags
)


@soc_net_router.get('/get')
async def get_social_network(name: Optional[str] = None) -> SocialNetwork | List[SocialNetwork]:
    if name:
        result = await org_service.soc_net_store.get(name)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await org_service.soc_net_store.get_all()
    return result


@soc_net_router.post('/add')
async def add_social_network(social_network: SocialNetwork, auth_user: User = Depends(get_auth_active_user)) -> None:
    await org_service.soc_net_store.add(social_network)


@soc_net_router.post('/edit')
async def edit_social_network(social_network: SocialNetwork, auth_user: User = Depends(get_auth_active_user)) -> None:
    await org_service.soc_net_store.edit(social_network)


@soc_net_router.get('/delete')
async def delete_social_network(name: str) -> None:
    await org_service.soc_net_store.delete(name=name)


org_router.include_router(soc_net_router)
