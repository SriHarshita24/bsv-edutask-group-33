import pytest

from unittest.mock import Mock
from unittest.mock import patch

from src.util.helpers import diceroll
from src.controllers.usercontroller import UserController


class TestNamespaces:

    @pytest.mark.namespaces
    def test_1(self):

        with patch('src.util.dao.DAO') as mockedDAO:

            mockedDAO.return_value = Mock()

            dao = mockedDAO()

            assert dao is not None

    @pytest.mark.namespaces
    def test_2(self):

        with patch('random.randint') as mockrandint:

            mockrandint.return_value = 5

            assert diceroll() is True

    @pytest.mark.namespaces
    def test_3(self):

        user = {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'jane.doe'
        }

        mockedDAO = Mock()
        mockedDAO.find.return_value = [user]

        uc = UserController(dao=mockedDAO)

        with patch('re.fullmatch') as mockfullmatch:

            mockfullmatch.return_value = True

            result = uc.get_user_by_email('jane.doe')

            assert result == user