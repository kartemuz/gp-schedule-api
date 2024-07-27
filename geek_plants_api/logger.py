import logging
from loguru import logger
from geek_plants_api.config import settings



logging.basicConfig(level=logging.INFO)
logger.add(f'{settings.LOG_DIR}/{settings.LOG_FILE_NAME}', format=settings.LOG_FORMAT, rotation=settings.LOG_ROTATION)
