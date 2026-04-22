import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


# TC1: one matching user
def test_get_user_by_email_single_match():
    dao = MagicMock()
    user = {"email": "test@mail.com"}
    dao.find.return_value = [user]

    controller = UserController(dao)
    result = controller.get_user_by_email("test@mail.com")

    assert result == user


# TC2: multiple matching users -> returns first
def test_get_user_by_email_multiple_matches():
    dao = MagicMock()
    user1 = {"email": "same@mail.com", "id": 1}
    user2 = {"email": "same@mail.com", "id": 2}
    dao.find.return_value = [user1, user2]

    controller = UserController(dao)
    result = controller.get_user_by_email("same@mail.com")

    assert result == user1


# TC3: no users found -> current code causes IndexError
def test_get_user_by_email_no_match():
    dao = MagicMock()
    dao.find.return_value = []

    controller = UserController(dao)

    with pytest.raises(IndexError):
        controller.get_user_by_email("nouser@mail.com")


# TC4: invalid email
def test_get_user_by_email_invalid_email():
    controller = UserController(MagicMock())

    with pytest.raises(ValueError):
        controller.get_user_by_email("wrongemail")


# TC5: empty email
def test_get_user_by_email_empty_email():
    controller = UserController(MagicMock())

    with pytest.raises(ValueError):
        controller.get_user_by_email("")


# TC6: database failure
def test_get_user_by_email_database_error():
    dao = MagicMock()
    dao.find.side_effect = Exception("DB Failed")

    controller = UserController(dao)

    with pytest.raises(Exception):
        controller.get_user_by_email("test@mail.com")