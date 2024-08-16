from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List, Final
from src.user.schemas import User, Opportunity, Role
from src.auth.dependencies import get_auth_active_user
from src.user.service import user_service


TAG: Final = 'user'

user_router = APIRouter(
    prefix='/user',
    tags=[TAG]
)


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
async def add_user(user: User, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.user_store.add(user)


@user_router.post('/edit')
async def edit_user(user: User, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.user_store.edit(user)


@user_router.post('/delete')
async def delete_user(login: str, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.user_store.delete_user(login)


opportunity_router = APIRouter(
    prefix="/opportunity",
    tags=[TAG]
)


@opportunity_router.get('/get')
async def get_opportunity(name: Optional[str] = None, auth_user: User = Depends(get_auth_active_user)) -> Opportunity | List[Opportunity]:
    if name:
        result = await user_service.opportunity_store.get(name)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await user_service.opportunity_store.get_all()
    return result


role_router = APIRouter(
    prefix="/role",
    tags=[TAG]
)


@role_router.get('/get')
async def get_role(name: Optional[str] = None, auth_user: User = Depends(get_auth_active_user)) -> Role | List[Role]:
    if name:
        result = await user_service.role_store.get(name=name)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        result = await user_service.role_store.get_all()
    return result


@role_router.post('/add')
async def add_role(role: Role, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.role_store.add(role)


@role_router.post('/edit')
async def edit_role(role: Role, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.role_store.edit(role)


@role_router.get('/delete')
async def delete_role(role: Role, auth_user: User = Depends(get_auth_active_user)) -> None:
    await user_service.role_store.delete(role)


user_router.include_router(opportunity_router)
user_router.include_router(role_router)