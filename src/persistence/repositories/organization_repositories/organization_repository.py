from src.core.stores.organization_stores import OrganizationStore
from src.core.schemes.organization import Organization
from src.persistence.database import session_factory
from src.persistence.database.models.organization_models import OrganizationDB, SocialNetworkDB
from src.persistence.exceptions import IntegrityError
from src.persistence.repositories.organization_repositories.social_network_repository import SocialNetworkRepository
from src.config import settings
from src.persistence.database.database_utils import BaseQueries


class OrganizationRepository(OrganizationStore):
    scheme = Organization
    model = OrganizationDB

    async def add(self, obj: scheme) -> None:
        async with session_factory() as session:
            organization_db = self.model(
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

    async def get(self, name: str = settings.ORGANIZATION_NAME) -> scheme:
        result: self.scheme
        organization_db = await BaseQueries.select_by_name(model=self.model, name=name)
        social_networks = await SocialNetworkRepository().get_all()

        result = self.scheme(
            email=organization_db.email,
            name=organization_db.name,
            address=organization_db.address,
            phone=organization_db.phone,
            social_networks=social_networks
        )

        return result

    async def edit(self, obj: scheme) -> None:
        await self.delete(name=obj.name)
        await self.add(obj)
        all_s_c_name = await BaseQueries.select_all_name(model=SocialNetworkDB)
        for name in all_s_c_name:
            await SocialNetworkRepository().delete(name=name)
        for s_c in obj.social_networks:
            await SocialNetworkRepository().add(s_c)

    async def delete(self, name: str = settings.ORGANIZATION_NAME) -> None:
        await BaseQueries.delete_by_name(model=self.model, name=name)
