from src.application.services import UserService, AuthService
from src.persistence.repositories.user_repositories import (
    ActionRepository,
    EntityRepository,
    OpportunityRepository,
    RoleRepository,
    UserRepository
)
from src.core.schemes.user import User, Opportunity, Role
from typing import List
from src.presentation.exceptions import NotValidPasswordException, NotValidLoginException, UserNotActiveException
from src.persistence.exceptions import IntegrityError
from src.presentation.controllers.auth_controller import AuthController


class UserController:
    user_service: UserService
    auth_controller: AuthController

    def __init__(self) -> None:
        self.user_service = UserService(
            action_repository=ActionRepository,
            entity_repository=EntityRepository,
            opportunity_repository=OpportunityRepository,
            role_repository=RoleRepository,
            user_repository=UserRepository
        )
        self.auth_controller = AuthController()

    async def get_user(self, login: str) -> User:
        # self.auth_controller.authorize(token)
        result: User = await self.user_service.user_store.get(login)
        return result

    async def get_all_users(self) -> List[User]:
        # self.auth_controller.authorize(token)
        result: List[User] = await self.user_service.user_store.get_all()
        return result

    async def add_user(self, user: User) -> None:
        # self.auth_controller.authorize(token)
        await self.user_service.user_store.add(user)

    async def edit_user(self, user: User) -> None:
        # self.auth_controller.authorize(token)
        await self.user_service.user_store.edit(user)

    async def delete_user(self, login: User) -> None:
        # self.auth_controller.authorize(token)
        await self.user_service.user_store.delete(login)

    async def get_opportunity(self, name: str) -> Opportunity:
        # self.auth_controller.authorize(token)
        result: Opportunity = await self.user_service.opportunity_store.get(name)
        return result

    async def get_all_opportunities(self) -> List[Opportunity]:
        # self.auth_controller.authorize(token)
        result: List[Opportunity] = await self.user_service.opportunity_store.get_all()
        return result

    async def add_opportunity(self, opportunity: Opportunity) -> None:
        # self.auth_controller.authorize(token)
        await self.user_service.opportunity_store.add(opportunity)
