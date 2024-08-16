from fastapi import APIRouter, Depends
from src.auth.schemas import Token
from src.auth.dependencies import validate_auth_user
from src.user.schemas import User
from src.auth.utils import JWTUtils

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


@auth_router.post('/login')
def login(
    user: User = Depends(validate_auth_user)
) -> Token:
    jwt_payload = {
        'sub': user.login,
        'username': user.login,
        'email': user.email
    }
    return Token(
        token=JWTUtils.encode_jwt(payload=jwt_payload)
    )
