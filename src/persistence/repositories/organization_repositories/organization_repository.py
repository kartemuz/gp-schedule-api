from src.core.stores.organization_stores import OrganizationStore
from src.core.schemes.organization import Organization, SocialNetwork
from typing import List, Optional
from src.persistence.database import session_factory, BaseSelect
from src.persistence.database.models.organization_models import OrganizationDB, SocialNetworkDB
from src.persistence.exceptions import IntegrityError
from src.persistence.repositories.organization_repositories.social_network_repository import SocialNetworkRepository
from src.config import settings

STORE = OrganizationStore
MODEL = OrganizationDB


class OrganizationRepository(STORE):
    scheme = Organization

    async def add(self, obj: scheme) -> None:
        async with session_factory() as session:
            organization_db: MODEL = MODEL(
                name=obj.name,
                address=obj.address,
                phone=obj.phone,
                email=obj.email
            )
            session.add(organization_db)
            try:
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                raise ex

            for s_n in obj.social_networks:
                await SocialNetworkRepository().add(s_n)

            try:
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                raise ex

    async def get(self, name: str = settings.ORGANIZATION_NAME) -> Optional[scheme]:
        result: Optional[self.scheme]
        organization_db: MODEL = await BaseSelect.select_by_name(model=MODEL, name=name)
        if organization_db is not None:
            social_networks: List[self.scheme] = []
            social_networks_db = await BaseSelect.select_all(model=SocialNetworkDB)
            for s_n_db in social_networks_db:
                social_networks.append(
                    SocialNetwork(
                        name=s_n_db.name,
                        value=s_n_db.value
                    )
                )

            result = self.scheme(
                email=organization_db.email,
                name=organization_db.name,
                address=organization_db.address,
                phone=organization_db.phone,
                social_networks=social_networks
            )
        else:
            result = None

        return result

    async def edit(self, obj: scheme) -> None:
        await self.delete(name=obj.name)
        await self.add(obj)

    async def delete(self, name: str = settings.ORGANIZATION_NAME) -> None:
        await BaseSelect.delete_by_name(model=MODEL, name=name)
