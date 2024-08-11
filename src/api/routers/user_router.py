from fastapi import APIRouter, Depends, HTTPException, status
from src.presentation.controllers import UserController
from src.core.schemes.user import User, Opportunity
from typing import Optional
from src.application.auth.auth_utils import JWTUtils
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List

user_controller = UserController()
http_bearer = HTTPBearer()
USER_TAG = 'user'

user_router = APIRouter(
    prefix="/user",
    tags=[USER_TAG]
)


@user_router.get('/get')
async def get_user(login: Optional[str] = None, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> User | List[User]:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    try:
        if login is not None:
            return await user_controller.get_user(login)
        else:
            return await user_controller.get_all_users()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@user_router.post('/add')
async def add_user(user: User, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    await user_controller.add_user(user)


@user_router.post('/edit')
async def edit_user(user: User, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    await user_controller.edit_user(user)


@user_router.post('/delete')
async def delete_user(login: str, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> None:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    await user_controller.delete_user(login)


opportunity_router = APIRouter(
    prefix="/opportunities",
    tags=[USER_TAG]
)


@opportunity_router.get('/get')
async def get_opportunity(name: Optional[str] = None, cred: HTTPAuthorizationCredentials = Depends(http_bearer)) -> Opportunity | List[Opportunity]:
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    if name is not None:
        return await user_controller.get_opportunity(name)
    else:
        return await user_controller.get_all_opportunities()


@opportunity_router.post('/add')
async def add_opportunity(opportunity: Opportunity, cred: HTTPAuthorizationCredentials = Depends(http_bearer)):
    try:
        JWTUtils.decode_jwt(token=cred.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    await user_controller.add_opportunity(opportunity)


user_router.include_router(opportunity_router)
