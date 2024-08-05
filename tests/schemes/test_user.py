import pytest
from src.core.schemes.user import Action, Entity, Opportunity, Role, User
from src.core.exceptions import ValidationError
from src.core.exceptions import EmailNotValidError, ValidationError
from contextlib import nullcontext as does_not_raise


class TestUser:
    @pytest.mark.parametrize(
        'id, name, excpectation',
        [
            (1, 'create', does_not_raise()),
            (2, 'delete', does_not_raise()),
            ('3', '3', does_not_raise()),
            (4, None, pytest.raises(ValidationError)),
            (5, 5, pytest.raises(ValidationError)),
        ]
    )
    def test_action(self, id, name, excpectation):
        with excpectation:
            obj = Action(name=name, id=id)
            assert obj.id == int(id)
            assert obj.name == name
            assert type(obj.id) == int

    @pytest.mark.parametrize(
        'id, name, excpectation',
        [
            (1, 'create', does_not_raise()),
            (2, 'delete', does_not_raise()),
            ('3', '3', does_not_raise()),
            (4, None, pytest.raises(ValidationError)),
            (5, 5, pytest.raises(ValidationError)),
        ]
    )
    def test_entity(self, id, name, excpectation):
        with excpectation:
            obj = Entity(name=name, id=id)
            assert obj.id == int(id)
            assert obj.name == name
            assert type(obj.id) == int

    @pytest.mark.parametrize(
        'id, code, action, entity, excpectation',
        [
            (1, '2', None, None, pytest.raises(ValidationError)),
            (2, 'code2', None, None, pytest.raises(ValidationError)),
            (3, 'code3', None, None, pytest.raises(ValidationError))
        ]
    )
    def test_ex_opportunity(self, id, code, action, entity, excpectation):
        with excpectation:
            obj = Opportunity(id=id, name=code, action=action, entity=entity)

    @pytest.mark.parametrize(
        'id, code, excpectation',
        [
            (1, '2', does_not_raise()),
            (2, 'code2', does_not_raise()),
            (3, 'code3', does_not_raise()),
            (4, 4, pytest.raises(ValidationError))
        ]
    )
    def test_opportunity(self, id, code, excpectation, actions, entities):
        with excpectation:
            for act in actions:
                for ent in entities:
                    obj = Opportunity(id=id, name=code, action=act, entity=ent)

    @pytest.mark.parametrize(
        'id, name, excpectation',
        [
            (1, 'name1', does_not_raise()),
            (2, 'name2', does_not_raise()),
            (3, 'name3', does_not_raise()),
            (4, 'name4', does_not_raise())
        ]
    )
    def test_role(self, id, name, excpectation, opportunities):
        with excpectation:
            obj = Role(id=id, name=name, opportunities=opportunities)

    @pytest.mark.parametrize(
        'id, login, email, password, excpectation',
        [
            (1, 'login1', 'bad-email', 'password1',
             pytest.raises(EmailNotValidError)),
            (2, 'login2', 'emai2l-test@test.ru', 'password2', does_not_raise()),
            (3, 'login3', 'email3-test@test.ru', 'password3', does_not_raise()),
            (4, 'login4', 'email4-test@test.ru', 'password4', does_not_raise())
        ]
    )
    def test_user(self, id, login, email, password, excpectation, roles, full_names):
        with excpectation:
            for r in roles:
                for fn in full_names:
                    obj = User(id=id, role=r, login=login, email=email,
                               hashed_password=password, full_name=fn)
