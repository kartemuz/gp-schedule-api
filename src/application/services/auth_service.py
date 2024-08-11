from src.application.auth import JWTUtils, PasswordUtils


class AuthService:
    jwt_utils: JWTUtils
    password_utils: PasswordUtils

    def __init__(self) -> None:
        self.jwt_utils = JWTUtils()
        self.password_utils = PasswordUtils()
