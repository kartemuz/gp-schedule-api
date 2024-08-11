import pytest
from src.persistence.repositories.user_repositories import (
    UserRepository,
    RoleRepository,
    ActionRepository,
    EntityRepository,
    OpportunityRepository
)
import asyncio
from loguru import logger


class TestUserRepository:

    def test_action_repository_add(self, actions):
        for ac in actions:
            asyncio.get_event_loop().run_until_complete(
                ActionRepository().add(obj=ac))

    def test_entity_repository_add(self, entities):
        for en in entities:
            asyncio.get_event_loop().run_until_complete(
                EntityRepository().add(obj=en))

    def test_opportunity_repository_add(self, opportunities):
        opportunity_repository = OpportunityRepository()
        for op in opportunities:
            asyncio.get_event_loop().run_until_complete(
                opportunity_repository.add(obj=op))

    def test_role_repository_add(self, roles):
        role_repository = RoleRepository()
        for r in roles:
            asyncio.get_event_loop().run_until_complete(
                role_repository.add(obj=r))

    def test_user_repository_add(self, users):
        user_repository = UserRepository()
        for u in users:
            asyncio.get_event_loop().run_until_complete(
                user_repository.add(obj=u))
