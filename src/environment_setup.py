import shutil
import os
import asyncio
from loguru import logger
from src.config import settings
from src.persistence.database.base import engine, BaseDB
from src.persistence.database.models import user_models, organization_models
from src.persistence.repositories.user_repositories import UserRepository
from src.core.schemes.user import User
from src.core.schemes.full_name import FullName
from src.application.auth.auth_utils import PasswordUtils


@logger.catch
def setup_logger() -> None:
    sink = f'{settings.LOG_DIR}/{settings.LOG_FILE_NAME}'
    format_ = settings.LOG_FORMAT
    rotation = settings.LOG_ROTATION
    level = 'DEBUG' if settings.DEBUG_STATUS else 'INFO'

    logger.add(sink=sink, format=format_, rotation=rotation, level=level)


@logger.catch
def setup_file_system() -> None:
    if os.path.exists(settings.LOG_DIR) and os.path.isdir(settings.LOG_DIR):
        shutil.rmtree(settings.LOG_DIR)


@logger.catch
async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)


@logger.catch
async def create_admin() -> None:
    admin = User(
        role=None,
        login=settings.ADMIN_LOGIN,
        hashed_password=PasswordUtils.hash_password(settings.ADMIN_PASSWORD),
        email=settings.ADMIN_EMAIL,
        full_name=FullName(surname=None, name='admin', patronymic=None),
        active=True,
        admin=True
    )
    await UserRepository().add(admin)


@logger.catch
async def setup_environment() -> None:
    setup_file_system()
    setup_logger()
    await setup_db()
    await create_admin()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(setup_environment())
