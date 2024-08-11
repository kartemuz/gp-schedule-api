from src.core.stores.user_stores import UserStore
from src.core.schemes.user import User
from src.core.schemes.full_name import FullName
from src.persistence.database.models.user_models import UserDB
from typing import List
from sqlalchemy import select
from src.persistence.database import session_factory
from src.persistence.repositories.user_repositories import RoleRepository
from src.persistence.exceptions import IntegrityError


class UserRepository(UserStore):
    scheme = User
    model = UserDB

    async def add(self, obj: scheme) -> None:
        if obj.role is not None:
            await RoleRepository().add(obj=obj.role)
            role_name = obj.role.name
        else:
            role_name = None
        async with session_factory() as session:
            user_db = UserDB(
                login=obj.login,
                email=obj.email,
                hashed_password=obj.hashed_password,
                surname=obj.full_name.surname,
                name=obj.full_name.name,
                patronymic=obj.full_name.patronymic,
                role_name=role_name,
                admin=obj.admin
            )

            session.add(user_db)
            try:
                await session.commit()

            except IntegrityError as ex:
                await session.rollback()
                raise ex

    async def get(self, login: str) -> scheme:
        result: self.scheme

        async with session_factory() as session:
            query = select(self.model).where(self.model.login == login)
            query_result = await session.execute(query)
            user_db = query_result.scalar()
            if user_db.role_name is not None:
                role = await RoleRepository().get(name=user_db.role_name)
            else:
                role = None
            result = self.scheme(
                role=role,
                login=user_db.login,
                email=user_db.email,
                hashed_password=user_db.hashed_password,
                full_name=FullName(
                    surname=user_db.surname,
                    name=user_db.name,
                    patronymic=user_db.patronymic
                ),
                active=user_db.active,
                admin=user_db.admin
            )
        return result

    async def edit(self, obj: scheme) -> None:
        await self.delete(login=obj.login)
        await self.add(obj=obj)

    async def delete(self, login: str) -> None:
        async with session_factory() as session:

            query_user = select(self.model).where(self.model.login == login)
            qeury_user_result = await session.execute(query_user)
            user_db = qeury_user_result.scalar()

            await session.delete(user_db)
            await session.commit()

    async def get_all(self) -> List[scheme]:
        result: List[self.scheme] = []
        async with session_factory() as session:
            query_all_logins = select(self.model.name)
            query_all_logins_result = await session.execute(query_all_logins)
            all_logins_db: List[str] = query_all_logins_result.scalars()
        for login in all_logins_db:
            result.append(
                await self.get(login=login)
            )
        return result
