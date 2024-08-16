import bcrypt
import jwt
from src.config import settings
from datetime import datetime, timedelta


class JWTUtils:
    @staticmethod
    def encode_jwt(
        payload: dict,
        private_key: str = settings.auth.private_key_path.read_text(),
        algorithm: str = settings.auth.token_algorithm,
        expire_minutes: int = settings.auth.token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(exp=expire, iat=now)
        return jwt.encode(to_encode, private_key, algorithm=algorithm)

    @staticmethod
    def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth.public_key_path.read_text(),
        algorithm: str = settings.auth.token_algorithm,
    ) -> dict:
        return jwt.decode(token, public_key, algorithms=[algorithm])


class PasswordUtils:
    @staticmethod
    def hash_password(
        password: str,
    ) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
