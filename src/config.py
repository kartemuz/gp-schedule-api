from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import BaseModel, EmailStr

BASE_DIR: Path = Path(__file__).parent.parent
ENV_PATH: Path = BASE_DIR / '.env'
TEST_ENV_PATH: Path = BASE_DIR / '.test.env'


class EmailSettings(BaseModel):
    login: str
    password: str


class DatabaseSettings(BaseModel):
    name: str
    host: str
    port: int
    user: str
    password: str

    repr_cols_num: int = 4

    short_string_length: int = 100
    long_string_length: int = 1000

    @property
    def url(self) -> str:
        return f'mysql+aiomysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}?charset=utf8mb4'


class AuthSettings(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    token_algorithm: str = 'RS256'
    token_expire_minutes: int = 60 * 24 * 365 * 10
    token_type: str = 'Bearer'


# class AdminSettings(BaseModel):
#     login: str
#     password: str
#     email: EmailStr


class OrganizationSettings(BaseModel):
    # name: str
    id: int


class ClientSettings(BaseModel):
    ip: str


class StaticSettings(BaseModel):
    dir_name: str

    @property
    def dir_path(self) -> Path:
        return BASE_DIR / self.dir_name


class ScheduleSettings(BaseModel):
    base_flow_prefix: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='CONFIG__'
    )
    debug: bool
    test: bool

    db: DatabaseSettings
    auth: AuthSettings = AuthSettings()
    # admin: AdminSettings
    org: OrganizationSettings
    client: ClientSettings
    email: EmailSettings
    static: StaticSettings
    schedule: ScheduleSettings


settings = Settings()
