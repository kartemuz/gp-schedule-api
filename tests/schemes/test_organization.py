import pytest
from src.core.schemes.organization import SocialNetwork, Organization
from src.core.exceptions import ValidationError
from contextlib import nullcontext as does_not_raise


class TestOrganization:
    @pytest.mark.parametrize(
        'name, value, excpectation',
        [
            ('tg1', 'link1', does_not_raise()),
            ('vk2', 'link2', does_not_raise()),
            ('vk3', 'link3', does_not_raise()),
            ('tg4', 23, pytest.raises(ValidationError)),
            (5, 3, pytest.raises(ValidationError)),
        ]
    )
    def test_social_network(self, name, value, excpectation):
        with excpectation:
            obj = SocialNetwork(name=name, value=value)
            assert obj.name == name

    @pytest.mark.parametrize(
        'name, address, phone, email, excpectation',
        [
            ('address1', 'name', '1234546456',
             'www@email.com', does_not_raise()),
            ('address2', 'name', '1234546456',
             'www@email.com', does_not_raise()),
            ('address2', 'name', '1234546456', 'il.com',
             pytest.raises(ValidationError)),
            (3, 'name', None, 'www@email.com', pytest.raises(ValidationError)),
            (None, 'name', '1234546456', 'www@email.com',
             pytest.raises(ValidationError)),
            (5, 'name', '1234546456', 'www@email.com',
             pytest.raises(ValidationError)),
        ]
    )
    def test_organization(self, name, address, phone, email, excpectation, social_networks):
        with excpectation:
            obj = Organization(name=name, address=address, phone=phone,
                               email=email, social_networks=social_networks)
