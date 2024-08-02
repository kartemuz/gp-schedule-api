from typing import Final
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DEBUG_STATUS: Final = True
    TEST_STATUS: Final = True
    ENV_PATH: Final = '.env' if TEST_STATUS == False else '.test.env'

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    STATIC_DIR: Final = 'static'

    LOG_DIR: Final = 'logs'
    LOG_FORMAT: Final = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | " \
                        "<level>{level: <8}</level> | " \
                        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_ROTATION: Final = '00:00'
    LOG_FILE_NAME: Final = '{time}.log' if TEST_STATUS is False else 'test.log'

    @property
    def db_url(self) -> str:
        result: str
        db_name: Final = 'mysql'
        db_engine: Final = 'aiomysql'
        charset: Final = 'utf8mb4'
        result = f'{db_name}+{db_engine}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?charset={charset}'
        return result

    model_config = SettingsConfigDict(
        env_file=ENV_PATH
    )


settings = Settings()
