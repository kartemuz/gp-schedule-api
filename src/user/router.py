from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List, Final
from src.user.schemas import RoleInput, UserInput, User, Opportunity, Role, UserChangePassword
from src.auth.dependencies import get_auth_active_user
from src.user.service import user_service
from src.auth.utils import PasswordUtils
from src.schemas import IdSchema
from src.email_app.service import email_service


tags: Final = ['user']

user_router = APIRouter(
    prefix='/user',
    tags=tags,
)


@user_router.post('/change_password')
async def change_password(
    user_change_password: UserChangePassword,
    auth_user: User = Depends(get_auth_active_user)
) -> None:
    user = await user_service.user_store.get(user_change_password.login)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_input = UserInput(
        login=user.login,
        email=user.email,
        hashed_password=PasswordUtils.hash_password(
            user_change_password.hashed_password
        ),
        full_name=user.full_name,
        active=user.active,
        role=IdSchema(
            id=user.role.id
        )
    )
    await user_service.user_store.edit(user_input)
    # email_service.send_email(
    #     email_=user_input.email,
    #     subject='Смена пароля',
    #     message=f'Новый пароль от аккаунта {user.login}: {user_change_password.hashed_password}'
    # )


@user_router.get('/get')
async def get_user(login: Optional[str] = None, auth_user: User = Depends(get_auth_active_user)) -> User | List[User]:
    if login:
        result = await user_service.user_store.get(login=login)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await user_service.user_store.get_all()
    return result


@user_router.post('/add')
async def add_user(user: UserInput, auth_user: User = Depends(get_auth_active_user)) -> None:
    user.hashed_password = PasswordUtils.hash_password(user.hashed_password)
    await user_service.user_store.add(user)


@user_router.post('/edit')
async def edit_user(user: UserInput, auth_user: User = Depends(get_auth_active_user)) -> None:
    '''The client transmits only the changed data, login is required'''
    await user_service.user_store.edit(user)


@user_router.post('/delete')
async def delete_user(login: str, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.user_store.delete_user(login)


opportunity_router = APIRouter(
    prefix="/opportunity",
    tags=tags
)


@opportunity_router.get('/get')
async def get_opportunity(id: Optional[str] = None, auth_user: User = Depends(get_auth_active_user)) -> Opportunity | List[Opportunity]:
    if id:
        result = await user_service.opportunity_store.get(id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await user_service.opportunity_store.get_all()
    return result


role_router = APIRouter(
    prefix="/role",
    tags=tags
)


@role_router.get('/get')
async def get_role(id: Optional[str] = None, auth_user: User = Depends(get_auth_active_user)) -> Role | List[Role]:
    if id:
        result = await user_service.role_store.get(id=id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await user_service.role_store.get_all()
    return result


@role_router.post('/add')
async def add_role(role: RoleInput, auth_user: User = Depends(get_auth_active_user)) -> IdSchema:
    return await user_service.role_store.add(role)


@role_router.post('/edit')
async def edit_role(role: RoleInput, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.role_store.edit(role)


@role_router.get('/delete')
async def delete_role(id: int, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.role_store.delete(id)


user_router.include_router(opportunity_router)
user_router.include_router(role_router)
