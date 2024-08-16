from pydantic import BaseModel
from pydantic import EmailStr


class UserLoginData(BaseModel):
    login: str
    password: str


class TokenPayload(BaseModel):
    sub: str
    login: str
    email: EmailStr


class Token(BaseModel):
    token: str
