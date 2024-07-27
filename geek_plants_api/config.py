# Конфигурационный файл


from typing import Final
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG_STATUS: Final = True
    DEV_STATUS: Final = True

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str

    STATIC_DIR: Final = 'static'

    LOG_DIR: Final = 'logs'
    LOG_FORMAT: Final = '{time} {level} {message}'
    LOG_ROTATION: Final = '00:00'
    LOG_FILE_NAME: Final = '{time}.log'

    @property
    def db_url(self) -> str:
        result: str
        db_name: Final = 'postgresql'
        db_engine: Final = 'asyncpg'
        result = f'{db_name}+{db_engine}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return result

    model_config = SettingsConfigDict(
        env_file='.env'
    )


settings = Settings()
