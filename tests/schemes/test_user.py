
import pytest
from src_old.core.schemes.user import Action, Entity, Opportunity, Role, User
from src_old.core.exceptions import ValidationError
from contextlib import nullcontext as does_not_raise


class TestUser:
    @pytest.mark.parametrize(
        'name, excpectation',
        [
            ('create', does_not_raise()),
            ('delete', does_not_raise()),
            ('3', does_not_raise()),
            (None, pytest.raises(ValidationError)),
            (5, pytest.raises(ValidationError)),
        ]
    )
    def test_action(self, name, excpectation):
        with excpectation:
            obj = Action(name=name)
            assert obj.name == name

    @pytest.mark.parametrize(
        'name, excpectation',
        [
            ('user', does_not_raise()),
            ('group', does_not_raise()),
            ('3', does_not_raise()),
            (None, pytest.raises(ValidationError)),
            (5, pytest.raises(ValidationError)),
        ]
    )
    def test_entity(self, name, excpectation):
        with excpectation:
            obj = Entity(name=name)
            assert obj.name == name

    @pytest.mark.parametrize(
        'name, action, entity, excpectation',
        [
            ('2', None, None, pytest.raises(ValidationError)),
            ('code2', None, None, pytest.raises(ValidationError)),
            ('code3', None, None, pytest.raises(ValidationError))
        ]
    )
    def test_ex_opportunity(self, name, action, entity, excpectation):
        with excpectation:
            obj = Opportunity(name=name, action=action, entity=entity)

    @pytest.mark.parametrize(
        'name, excpectation',
        [
            ('2', does_not_raise()),
            ('code2', does_not_raise()),
            ('code3', does_not_raise()),
            (4, pytest.raises(ValidationError))
        ]
    )
    def test_opportunity(self, name, excpectation, actions, entities):
        with excpectation:
            for act in actions:
                for ent in entities:
                    obj = Opportunity(name=name, action=act, entity=ent)

    @pytest.mark.parametrize(
        'name, excpectation',
        [
            ('name1', does_not_raise()),
            ('name2', does_not_raise()),
            ('name3', does_not_raise()),
            ('name4', does_not_raise())
        ]
    )
    def test_role(self, name, excpectation, opportunities):
        with excpectation:
            obj = Role(name=name, opportunities=opportunities)

    @pytest.mark.parametrize(
        'login, email, password, active, admin, excpectation',
        [
            ('login1', 'bad-email', 'password1', True, False, pytest.raises(
                ValidationError)),
            ('login2', 'emai2l-test@test.ru',
             'password2', True, False, does_not_raise()),
            ('login3', 'email3-test@test.ru',
             'password3', True, False, does_not_raise()),
            ('login4', 'email4-test@test.ru',
             'password4', True, False, does_not_raise())
        ]
    )
    def test_user(self, login, email, password, active, admin, excpectation, roles, full_names):
        with excpectation:
            for r in roles:
                for fn in full_names:
                    obj = User(role=r, login=login, email=email,
                               hashed_password=password, full_name=fn, active=active, admin=admin)
