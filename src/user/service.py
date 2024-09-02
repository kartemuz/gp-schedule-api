from src.user.stores import (
    ActionStore,
    EntityStore,
    OpportunityStore,
    RoleStore,
    UserStore
)

from src.user.repositories import (
    ActionRepos,
    EntityRepos,
    OpportunityRepos,
    RoleRepos,
    UserRepos
)


class UserService:
    action_store: ActionStore
    entity_store: EntityStore
    opportunity_store: OpportunityStore
    role_store: RoleStore
    user_store: UserStore

    def __init__(
        self,
        action_repository: ActionStore,
        entity_repository: EntityStore,
        opportunity_repository: OpportunityStore,
        role_repository: RoleStore,
        user_repository: UserStore
    ) -> None:
        self.action_store = action_repository()
        self.entity_store = entity_repository()
        self.opportunity_store = opportunity_repository()
        self.role_store = role_repository()
        self.user_store = user_repository()


user_service = UserService(
    action_repository=ActionRepos,
    entity_repository=EntityRepos,
    opportunity_repository=OpportunityRepos,
    role_repository=RoleRepos,
    user_repository=UserRepos
)
