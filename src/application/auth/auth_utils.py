from src.config import settings
from datetime import datetime, timedelta
from loguru import logger

import bcrypt
import jwt


class JWTUtils:
    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.TOKEN_ALGORITHM,
        expire_minutes: int = settings.TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        result: str
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire, iat=now)
        result = jwt.encode(to_encode, private_key, algorithm=algorithm, )
        return result

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.TOKEN_ALGORITHM,
    ) -> dict:
        result: dict = jwt.decode(token, public_key, algorithms=[algorithm])
        logger.debug(result)
        return result


class PasswordUtils:
    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        result: bytes
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        result = bcrypt.hashpw(pwd_bytes, salt)
        return result

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        result: bool = bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
        return result
