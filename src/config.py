from typing import Final
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR: Path = Path(__file__).parent.parent


class Settings(BaseSettings):

    DEBUG_STATUS: Final = True
    TEST_STATUS: Final = True
    ENV_PATH: Path = BASE_DIR / '.env' if TEST_STATUS is False else BASE_DIR / '.test.env'

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str

    ORGANIZATION_NAME: str

    STATIC_DIR: Path = BASE_DIR / 'static'

    PRIVATE_KEY_PATH: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    PUBLIC_KEY_PATH: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    TOKEN_ALGORITHM: Final = 'RS256'
    TOKEN_EXPIRE_MINUTES: Final = 60
    TOKEN_TYPE: str = 'Bearer'

    ADMIN_LOGIN: str
    ADMIN_PASSWORD: str
    ADMIN_EMAIL: str

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
