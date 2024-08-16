from src.org.repositories import OrgRepos, SocNetRepos
from src.org.stores import OrgStore, SocNetStore


class OrgService:
    org_store: OrgStore
    soc_net_store: SocNetStore

    def __init__(
        self,
        org_repos: OrgStore,
        soc_net_repos: SocNetRepos
    ) -> None:
        self.org_store = org_repos()
        self.soc_net_store = soc_net_repos()


org_service = OrgService(
    org_repos=OrgRepos,
    soc_net_repos=SocNetRepos
)
