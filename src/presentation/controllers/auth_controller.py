from src.application.services import AuthService, UserService
from src.presentation.exceptions import NotValidLoginException, NotValidPasswordException, UserNotActiveException
from src.persistence.exceptions import IntegrityError
from src.core.schemes.user import User
from src.persistence.repositories.user_repositories import (
    ActionRepository,
    EntityRepository,
    OpportunityRepository,
    RoleRepository,
    UserRepository
)
from src.presentation.exceptions import InvalidTokenError
from loguru import logger


class AuthController:
    auth_service: AuthService
    user_service: UserService

    def __init__(self) -> None:
        self.auth_service = AuthService()
        self.user_service = UserService(
            action_repository=ActionRepository,
            entity_repository=EntityRepository,
            opportunity_repository=OpportunityRepository,
            role_repository=RoleRepository,
            user_repository=UserRepository
        )

    async def get_token(self, login: str, password: str) -> str:
        result: str
        try:
            user: User = await self.user_service.user_store.get(login=login)
        except IntegrityError:
            raise NotValidLoginException
        if not self.auth_service.password_utils.validate_password(
            password=password,
            hashed_password=user.hashed_password
        ):
            raise NotValidPasswordException
        if not user.active:
            raise UserNotActiveException

        jwt_payload = {
            'sub': user.login,
            'username': user.login,
            'email': user.email
        }
        result = self.auth_service.jwt_utils.encode_jwt(payload=jwt_payload)

        return result

    @logger.catch
    def authorize(self, token: str) -> None:
        self.auth_service.jwt_utils.decode_jwt(token=token,)
        # try:
        #     self.auth_service.jwt_utils.decode_jwt(token=token)
        # except InvalidTokenError as ex:
        #     logger.error(ex)
        #     raise ex
