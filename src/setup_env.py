from src.user import models
from src.org import models
from src.schedule import models
from src.database import engine, BaseDB
import asyncio
from src.user.service import user_service
from src.org.service import org_service
from pathlib import Path
from src.user.schemas import User
from pydantic import BaseModel
from typing import List
from src.auth.utils import PasswordUtils
from src.org.schemas import Organization


class SettingsJson(BaseModel):
    users: List[User]
    organization: Organization


json_path: Path = Path(__file__).parent.parent / 'settings.json'
settings_json: SettingsJson = SettingsJson.parse_file(json_path)


async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)


async def create_users() -> None:
    for u in settings_json.users:
        u.hashed_password = PasswordUtils.hash_password(
            u.hashed_password.decode()
        )
        await user_service.user_store.add(u)


async def create_organization() -> None:
    await org_service.org_store.add(settings_json.organization)


async def setup_env() -> None:
    await setup_db()
    await create_users()
    await create_organization()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(setup_env())
