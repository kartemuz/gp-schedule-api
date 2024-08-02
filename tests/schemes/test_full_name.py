import pytest
from src.core.schemes.full_name import FullName
from contextlib import nullcontext as does_not_raise
from pydantic import ValidationError


class TestFullName:
    @pytest.mark.parametrize(
        'surname, name, patronymic, expectation',
        [
            ('surname1', 'name1', 'patronymic1', does_not_raise()),
            ('surname2', 'name2', None, does_not_raise()),
            ('surname3', None, 'patronymic3', does_not_raise()),
            (None, 'name4', 'patronymic4', does_not_raise()),
            (None, None, None, does_not_raise()),
            (1, 1, 1, pytest.raises(ValidationError))
        ]
    )
    def test_init(self, surname, name, patronymic, expectation):
        with expectation:
            obj = FullName(
                surname=surname,
                name=name,
                patronymic=patronymic
            )
            assert obj.surname == surname
            assert obj.name == name
            assert obj.patronymic == patronymic
