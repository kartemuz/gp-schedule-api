from src.core.stores.organization_stores import SocialNetworkStore
from src.core.schemes.organization import SocialNetwork
from typing import List
from src.persistence.database.models.organization_models import SocialNetworkDB
from src.persistence.database import session_factory
from src.persistence.database.database_utils import BaseQueries
from src.persistence.exceptions import IntegrityError


class SocialNetworkRepository(SocialNetworkStore):
    scheme = SocialNetwork
    model = SocialNetworkDB

    async def add(self, obj: scheme) -> None:
        async with session_factory() as session:
            social_network_db: self.model = self.model(
                name=obj.name,
                value=obj.value
            )
            session.add(social_network_db)
            try:
                await session.commit()

            except IntegrityError as ex:
                await session.rollback()
                # raise ex

    async def get(self, name: str) -> scheme:
        result: self.scheme
        social_network_db: self.model = await BaseQueries.select_by_name(model=self.model, name=name)
        result = self.scheme(
            name=social_network_db.name,
            value=social_network_db.value
        )
        return result

    async def edit(self, obj: scheme) -> None:
        await self.delete(name=obj.name)
        await self.add(obj)

    async def delete(self, name: str) -> None:
        await BaseQueries.delete_by_name(model=self.model, name=name)

    async def get_all(self) -> List[scheme]:
        social_networks_db = await BaseQueries.select_all(self.model)
        result = []
        for s_n_db in social_networks_db:
            result.append(
                SocialNetwork(name=s_n_db.name, value=s_n_db.value)
            )
        return result
