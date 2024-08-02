import shutil
import os
import asyncio
from loguru import logger
from src.config import settings
from src.persistence.database.base import engine, BaseDB
from src.persistence.database.models.user import (
    ActionDB,
    EntityDB,
    OpportunityDB,
    RoleOpportunityDB,
    RoleDB,
    UserDB
)


def setup_logger() -> None:
    sink = f'{settings.LOG_DIR}/{settings.LOG_FILE_NAME}'
    format_ = settings.LOG_FORMAT
    rotation = settings.LOG_ROTATION
    level = 'DEBUG' if settings.DEBUG_STATUS else 'INFO'

    logger.add(sink=sink, format=format_, rotation=rotation, level=level)


def setup_file_system() -> None:
    if os.path.exists(settings.LOG_DIR) and os.path.isdir(settings.LOG_DIR):
        shutil.rmtree(settings.LOG_DIR)


async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)


async def setup_environment() -> None:
    setup_file_system()
    setup_logger()
    await setup_db()


if __name__ == '__main__':
    asyncio.run(setup_environment())
