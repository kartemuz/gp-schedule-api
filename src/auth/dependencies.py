from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from src.auth.schemas import UserLoginData
from src.user.schemas import User
from src.user.service import user_service
from src.auth.utils import PasswordUtils, JWTUtils
from src.exceptions import IntegrityError
from src.auth.exceptions import DecodeError

http_bearer = HTTPBearer()


async def validate_auth_user(
    user_login_data: UserLoginData
) -> User:
    try:
        user = await user_service.user_store.get(login=user_login_data.login)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Not valid login')
    if not PasswordUtils.validate_password(password=user_login_data.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Not valid password'
        )
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='User not active'
        )
    return user


def get_token(
    creds: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> str:
    return creds.credentials


def get_token_payload(
    token: str = Depends(get_token)
) -> dict:
    try:
        return JWTUtils.decode_jwt(token=token)
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Bad token'
        )


async def get_auth_active_user(
    token_payload: dict = Depends(get_token_payload)
) -> User:
    return await user_service.user_store.get(login=token_payload.get('username'))
