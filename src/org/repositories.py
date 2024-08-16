from src.org.schemas import Organization, SocialNetwork
from src.org.models import OrgDB, SocNetDB
from src.org.stores import OrgStore, SocNetStore
from src.database import session_factory
from src.exceptions import IntegrityError
from src.utils import DBUtils
from typing import List
from src.config import settings


class SocNetRepos(SocNetStore):
    async def add(self, obj: SocialNetwork) -> None:
        async with session_factory() as session:
            soc_net_db: SocNetDB = SocNetDB(
                name=obj.name,
                value=obj.value
            )
            session.add(soc_net_db)
            try:
                await session.commit()

            except IntegrityError:
                await session.rollback()

    async def get(self, name: str) -> SocialNetwork:
        soc_net_db: SocNetDB = await DBUtils.select_by_name(model=SocNetDB, name=name)
        return SocialNetwork(
            name=soc_net_db.name,
            value=soc_net_db.value
        )

    async def edit(self, obj: SocialNetwork) -> None:
        await self.delete(name=obj.name)
        await self.add(obj)

    async def delete(self, name: str) -> None:
        await DBUtils.delete_by_name(model=SocNetDB, name=name)

    async def get_all(self) -> List[SocialNetwork]:
        soc_nets_db: List[SocNetDB] = await DBUtils.select_all(SocNetDB)
        result = []
        for s_n_db in soc_nets_db:
            result.append(
                SocialNetwork(name=s_n_db.name, value=s_n_db.value)
            )
        return result


soc_net_repos = SocNetRepos()


class OrgRepos(OrgStore):

    async def add(self, obj: Organization) -> None:
        async with session_factory() as session:
            org_db = OrgDB(
                name=obj.name,
                address=obj.address,
                phone=obj.phone,
                email=obj.email
            )
            session.add(org_db)
            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

            for s_n in obj.social_networks:
                await soc_net_repos.add(s_n)

            try:
                await session.commit()
            except IntegrityError:
                await session.rollback()

    async def get(self, name: str = settings.org.name) -> Organization:
        org_db = await DBUtils.select_by_name(model=OrgDB, name=name)
        soc_nets = await soc_net_repos.get_all()

        result = Organization(
            email=org_db.email,
            name=org_db.name,
            address=org_db.address,
            phone=org_db.phone,
            social_networks=soc_nets
        )

        return result

    async def edit(self, obj: Organization) -> None:
        await self.delete(name=obj.name)
        await self.add(obj)
        all_s_c_name = await DBUtils.select_all_name(model=SocNetDB)
        for name in all_s_c_name:
            await soc_net_repos.delete(name=name)
        for s_c in obj.social_networks:
            await soc_net_repos.add(s_c)

    async def delete(self, name: str = settings.org.name) -> None:
        await DBUtils.delete_by_name(model=SocNetDB, name=name)
