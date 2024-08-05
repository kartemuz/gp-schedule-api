import pytest
from src.persistence.repositories.organization_repositories import OrganizationRepository, SocialNetworkRepository
import asyncio
from loguru import logger


class TestOrganizatonRepository():
    def test_organization_repository_add(self, organization):
        organization_repository = OrganizationRepository()
        asyncio.get_event_loop().run_until_complete(
            organization_repository.add(organization))

    def test_organization_repository_get(self, organization):
        organization_repository = OrganizationRepository()
        asyncio.get_event_loop().run_until_complete(
            organization_repository.get(name=organization.name))
        asyncio.get_event_loop().run_until_complete(
            organization_repository.get())

    def test_organization_repository_edit(self, organization):
        organization_repository = OrganizationRepository()
        organization.social_networks = []
        asyncio.get_event_loop().run_until_complete(
            organization_repository.edit(obj=organization))

    # def test_social_network_repository_add(self, social_networks, organizations):
    #     social_networks_repository = SocialNetworkRepository()
    #     for org in organizations:
    #         for s_n in social_networks:
    #             asyncio.get_event_loop().run_until_complete(
    #                 social_networks_repository.add(obj=s_n, organization_id=org.id))
