import pytest
import inspect
import asyncio
from src.environment_setup import setup_environment
from loguru import logger
from src.config import settings
from src.core.schemes.user import Action, Entity, Opportunity, Role, User
from src.core.schemes.full_name import FullName
from src.core.schemes.organization import SocialNetwork, Organization
from src.application.auth import PasswordUtils


@pytest.fixture(scope='session', autouse=True)
def setup_env():
    assert settings.TEST_STATUS is True
    asyncio.get_event_loop().run_until_complete(setup_environment())
    logger.info(f'Launched {inspect.currentframe().f_code.co_name}')
    yield setup_env
    logger.info(f'Completed {inspect.currentframe().f_code.co_name}')


@pytest.fixture(scope='package', autouse=True)
def full_names():
    result = [
        FullName(surname='surname1', name='name1', patronymic='patronymic1'),
        FullName(surname='surname2', name='name2', patronymic=None),
        FullName(surname='surname3', name=None, patronymic='patronymic3'),
        FullName(name='name4', patronymic='patronymic4'),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def actions():
    result = [
        Action(name='create'),
        Action(name='delete'),
        Action(name='add'),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def entities():
    result = [
        Entity(name='user'),
        Entity(name='group'),
        Entity(name='teacher'),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def opportunities(actions, entities):
    result = [
        Opportunity(name='code1', action=actions[0], entity=entities[0]),
        Opportunity(name='code2', action=actions[0], entity=entities[1]),
        Opportunity(name='code3', action=actions[0], entity=entities[2]),
        Opportunity(name='code4', action=actions[1], entity=entities[1]),
        Opportunity(name='code5', action=actions[1], entity=entities[2]),
        Opportunity(name='code6', action=actions[2], entity=entities[0]),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def roles(opportunities):
    result = [
        Role(name='Admin', opportunities=opportunities),
        Role(name='User', opportunities=[opportunities[0], opportunities[1]])
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def users(full_names, roles):
    result = [
        User(
            email='admin1@geek-plants.ru',
            login='admin1',
            active=True,
            hashed_password=PasswordUtils.hash_password('password1'),
            role=roles[0],
            full_name=full_names[0],
            admin=False
        ),

        User(
            email='user1@geek-plants.ru',
            login='user2',
            active=True,
            hashed_password=PasswordUtils.hash_password('password2'),
            role=roles[1],
            full_name=full_names[2],
            admin=False
        )
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def social_networks():
    result = [
        SocialNetwork(name='tg1', value='link1'),
        SocialNetwork(name='vk2', value='link2'),
        SocialNetwork(name='vk3', value='link3'),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def organization(social_networks):
    result = Organization(address='address1', phone='1234546456',
                          email='www@email.com', social_networks=social_networks)
    return result
