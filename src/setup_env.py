from src.user import models
from src.org import models
from src.schedule import models
from src.database import engine, BaseDB
import asyncio
from src.user.service import user_service
from src.org.service import org_service
from pathlib import Path
from src.user.schemas import UserInput, Action, Entity, Opportunity, RoleInput
from pydantic import BaseModel
from typing import List
from src.auth.utils import PasswordUtils
from src.org.schemas import Organization
from src.schedule.schemas import Teacher, TypeDirection, TypeLesson, Discipline, DirectionInput
from src.schedule.service import schedule_service


class SettingsJson(BaseModel):
    disciplines: List[Discipline]
    type_lessons: List[TypeLesson]
    type_directions: List[TypeDirection]
    actions: List[Action]
    entities: List[Entity]
    opportunities: List[Opportunity]
    roles: List[RoleInput]
    users: List[UserInput]
    organization: Organization
    teachers: List[Teacher]
    directions: List[DirectionInput]


json_path: Path = Path(__file__).parent.parent / 'settings.json'
settings_json: SettingsJson = SettingsJson.parse_file(json_path)


async def setup_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(BaseDB.metadata.drop_all)
        await conn.run_sync(BaseDB.metadata.create_all)


async def create_directions() -> None:
    for d in settings_json.directions:
        await schedule_service.direction_store.add(d)


async def create_disciplines() -> None:
    for d in settings_json.disciplines:
        await schedule_service.discipline_store.add(d)


async def create_type_lessons() -> None:
    for t_l in settings_json.type_lessons:
        await schedule_service.type_lesson_store.add(t_l)


async def create_type_directons() -> None:
    for t_d in settings_json.type_directions:
        await schedule_service.type_direction_store.add(t_d)


async def create_actions() -> None:
    for a in settings_json.actions:
        await user_service.action_store.add(a)


async def create_entities() -> None:
    for e in settings_json.entities:
        await user_service.entity_store.add(e)


async def create_opportunities() -> None:
    for op in settings_json.opportunities:
        await user_service.opportunity_store.add(op)


async def create_roles() -> None:
    for r in settings_json.roles:
        await user_service.role_store.add(r)


async def create_users() -> None:
    for u in settings_json.users:
        u.hashed_password = PasswordUtils.hash_password(
            u.hashed_password
        )
        await user_service.user_store.add(u)


async def create_organization() -> None:
    await org_service.org_store.add(settings_json.organization)


async def create_teachers() -> None:
    for t in settings_json.teachers:
        await schedule_service.teacher_store.add(t)


async def setup_env() -> None:
    await setup_db()
    await create_actions()
    await create_entities()
    await create_opportunities()
    await create_roles()
    await create_users()
    await create_organization()
    await create_teachers()
    await create_type_directons()
    await create_type_lessons()
    await create_disciplines()
    await create_directions()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(setup_env())
