import pytest

from unittest.mock import patch

from src.util.helpers import diceroll


@pytest.mark.demo
@pytest.mark.parametrize(
    'value, expected',
    [
        (4, False),
        (5, True),
        (6, True)
    ]
)
def test_diceroll_success(value, expected):

    with patch('src.util.helpers.random.randint') as mockrandint:

        mockrandint.return_value = value

        assert diceroll() == expected