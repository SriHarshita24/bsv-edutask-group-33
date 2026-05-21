import pytest
from unittest.mock import MagicMock
from src.controllers.usercontroller import UserController


# ==================================================
# Fixtures
# ==================================================

@pytest.fixture
def dao():
    return MagicMock()


@pytest.fixture
def controller(dao):
    return UserController(dao)


# ==================================================
# TC1: Valid registered email with one matching user
# Expected Result: Return that user object
# ==================================================

def test_get_user_by_email_single_match(controller, dao):

    # Arrange
    user = {"email": "test@mail.com"}

    dao.find.return_value = [user]

    # Act
    result = controller.get_user_by_email("test@mail.com")

    # Assert
    assert result == user


# ==================================================
# TC2: Valid email with multiple matching users
# Expected Result: Return the first user object
# ==================================================

def test_get_user_by_email_multiple_matches(controller, dao):

    # Arrange
    user1 = {"email": "same@mail.com", "id": 1}
    user2 = {"email": "same@mail.com", "id": 2}

    dao.find.return_value = [user1, user2]

    # Act
    result = controller.get_user_by_email("same@mail.com")

    # Assert
    assert result == user1


# ==================================================
# TC3: Valid email with no matching users
# Expected Result: Return None
# ==================================================

def test_get_user_by_email_no_match(controller, dao):

    # Arrange
    dao.find.return_value = []

    # Act
    result = controller.get_user_by_email("nouser@mail.com")

    # Assert
    assert result is None


# ==================================================
# TC4: Invalid email format
# Expected Result: Raise ValueError
# ==================================================

def test_get_user_by_email_invalid_email(controller):

    # Act + Assert
    with pytest.raises(ValueError):
        controller.get_user_by_email("wrongemail")


# ==================================================
# TC5: Empty email string
# Expected Result: Raise ValueError
# ==================================================

def test_get_user_by_email_empty_email(controller):

    # Act + Assert
    with pytest.raises(ValueError):
        controller.get_user_by_email("")


# ==================================================
# TC6: Database operation failure
# Expected Result: Raise Exception
# ==================================================

def test_get_user_by_email_database_error(controller, dao):

    # Arrange
    dao.find.side_effect = Exception("DB Failed")

    # Act + Assert
    with pytest.raises(Exception):
        controller.get_user_by_email("test@mail.com")