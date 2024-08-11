from src.core.stores.organization_stores import OrganizationStore, SocialNetworkStore
from src.core.schemes.organization import Organization, SocialNetwork
from typing import Optional, List


class OrganizationService():
    organization_store: OrganizationStore
    social_network_store: SocialNetworkStore

    def __init__(self, organization_reposotory: OrganizationStore,
                 social_network_repository: SocialNetworkStore) -> None:
        self.organization_store = organization_reposotory()
        self.social_network_store = social_network_repository()

    # async def get_organization(self) -> Optional[Organization]:
    #     result: Organization = await self.organization_store.get()
    #     return result

    # async def add_organization(self, obj: Organization) -> None:
    #     await self.organization_store.add(obj)

    # async def edit_organization(self, obj: Organization) -> None:
    #     await self.organization_store.edit(obj)

    # async def get_social_network(self, name: str) -> Optional[SocialNetwork]:
    #     result: List[SocialNetwork] = await self.social_network_store.get(name=name)
    #     return result

    # async def get_all_social_networks(self) -> List[SocialNetwork]:
    #     result: List[SocialNetwork] = await self.social_network_store.get_all()
    #     return result

    # async def add_social_network(self, obj: SocialNetwork) -> None:
    #     await self.social_network_store.add(obj)

    # async def delete_social_network(self, name: str) -> None:
    #     await self.social_network_store.delete(name)

    # async def edit_social_network(self, obj: SocialNetwork) -> None:
    #     await self.social_network_store.edit(obj)
