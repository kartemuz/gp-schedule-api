from src.presentation.controllers import UserController, AuthController
import asyncio
import pytest
from contextlib import nullcontext as does_not_raise
from src.presentation.exceptions import NotValidPasswordException

user_controller = UserController()
auth_controller = AuthController()


class TestUserAuthController:
    def test_user_add(self, users):
        for u in users:
            asyncio.get_event_loop().run_until_complete(user_controller.add_user(u))

    @pytest.mark.parametrize(
        'password, expectation',
        [
            ('password1', does_not_raise()),
            ('badpassword', pytest.raises(NotValidPasswordException))
        ]
    )
    def test_auth_user(self, password, expectation, users):
        with expectation:
            u = users[0]
            asyncio.get_event_loop().run_until_complete(
                auth_controller.get_token(login=u.login, password=password))
