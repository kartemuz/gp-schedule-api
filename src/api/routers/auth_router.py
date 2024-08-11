from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from src.presentation.controllers import AuthController
from pydantic import BaseModel

auth_controller = AuthController()

AUTH_TAG = 'auth'

auth_router = APIRouter(
    prefix="/auth",
    tags=[AUTH_TAG]
)


class UserData(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    token: str


@auth_router.post('/login')
async def login(user_data: UserData) -> Token:
    try:
        return Token(token=await auth_controller.get_token(
            login=user_data.login,
            password=user_data.password)
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
