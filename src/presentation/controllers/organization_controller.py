from src.application.services import OrganizationService
from src.persistence.repositories.organization_repositories import OrganizationRepository, SocialNetworkRepository
from src.core.schemes.organization import Organization, SocialNetwork
from typing import List
from src.presentation.controllers.auth_controller import AuthController
from loguru import logger
from jwt.exceptions import InvalidTokenError, DecodeError


class OrganizationController:
    organization_service: OrganizationService
    auth_controller: AuthController

    def __init__(self) -> None:
        self.organization_service = OrganizationService(
            organization_reposotory=OrganizationRepository,
            social_network_repository=SocialNetworkRepository
        )
        self.auth_controller = AuthController()

    async def get_organization(self) -> Organization:
        result: Organization = await self.organization_service.organization_store.get()
        return result

    async def add_organization(self, obj: Organization) -> None:
        await self.organization_service.organization_store.add(obj)

    @logger.catch
    async def edit_organization(self, obj: Organization) -> None:
        # self.auth_controller.authorize(token)
        await self.organization_service.organization_store.edit(obj)

    async def get_social_network(self, name: str) -> SocialNetwork:
        result: List[SocialNetwork] = await self.organization_service.social_network_store.get(name=name)
        return result

    async def get_all_social_networks(self) -> List[SocialNetwork]:
        result: List[SocialNetwork] = await self.organization_service.social_network_store.get_all()
        return result

    async def add_social_network(self, obj: SocialNetwork) -> None:
        # try:
        #     self.auth_controller.authorize(token)
        # except DecodeError:
        #     raise DecodeError
        await self.organization_service.social_network_store.add(obj)

    async def delete_social_network(self, name: str) -> None:
        # self.auth_controller.authorize(token)
        await self.organization_service.social_network_store.delete(name)

    async def edit_social_network(self, obj: SocialNetwork) -> None:
        # self.auth_controller.authorize(token)
        await self.organization_service.social_network_store.edit(obj)
