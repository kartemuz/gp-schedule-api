import pytest
import inspect
from src.environment_setup import setup_environment
from loguru import logger
from src.config import settings
from src.core.schemes.user import Action, Entity, Opportunity, Role, User
from src.core.schemes.full_name import FullName


@pytest.fixture(scope='session', autouse=True)
async def setup_env():
    assert settings.TEST_STATUS == True
    await setup_environment()
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
        Action(id=1, name='create'),
        Action(id=2, name='delete'),
        Action(id='3', name='add'),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def entities():
    result = [
        Entity(id=1, name='user'),
        Entity(id=2, name='group'),
        Entity(id='3', name='teacher'),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def opportunities(actions, entities):
    result = [
        Opportunity(id=1, name='code1', action=actions[0], entity=entities[0]),
        Opportunity(id=2, name='code2', action=actions[0], entity=entities[1]),
        Opportunity(id=3, name='code3', action=actions[0], entity=entities[2]),
        Opportunity(id=1, name='code4', action=actions[1], entity=entities[1]),
        Opportunity(id=1, name='code5', action=actions[1], entity=entities[2]),
        Opportunity(id=1, name='code6', action=actions[2], entity=entities[0]),
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def roles(opportunities):
    result = [
        Role(id=1, name='Admin', opportunities=opportunities),
        Role(name='User', opportunities=[opportunities[0], opportunities[1]])
    ]
    return result


@pytest.fixture(scope='package', autouse=True)
def users(full_names, roles):
    result = [
        User(
            id=1,
            email='admin1@geek-plants.ru',
            login='admin1',
            hashed_password='password1',
            role=roles[0],
            full_name=full_names[0]
        ),

        User(
            id=2,
            email='user1@geek-plants.ru',
            login='user2',
            hashed_password='password2',
            role=roles[1],
            full_name=full_names[2]
        )
    ]
    return result
