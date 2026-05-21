import pytest
from unittest.mock import MagicMock, patch
from src.util.dao import DAO


# ==================================================
# Fixture
# ==================================================

@pytest.fixture
def dao():

    test_dao = DAO("user")

    # mock Mongo collection
    test_dao.collection = MagicMock()

    return test_dao


# ==================================================
# TC1: Valid data -> insert succeeds
# ==================================================

@patch("src.util.dao.getValidator")
def test_create_valid_data(mock_validator, dao):

    # Arrange
    mock_validator.return_value = {}

    data = {
        "name": "Alice",
        "active": True
    }

    dao.collection.insert_one.return_value.inserted_id = 1

    dao.collection.find_one.return_value = {
        "_id": 1,
        "name": "Alice",
        "active": True
    }

    dao.to_json = MagicMock(
        return_value={
            "_id": "1",
            "name": "Alice",
            "active": True
        }
    )

    # Act
    result = dao.create(data)

    # Assert
    assert result["name"] == "Alice"
    assert result["_id"] == "1"


# ==================================================
# TC2: Missing required field
# ==================================================

@patch("src.util.dao.getValidator")
def test_create_invalid_data(mock_validator, dao):

    # Arrange
    mock_validator.return_value = {}

    dao.collection.insert_one.side_effect = Exception("WriteError")

    # Act + Assert
    with pytest.raises(Exception):
        dao.create({
            "name": "OnlyName"
        })


# ==================================================
# TC3: Empty object
# ==================================================

@patch("src.util.dao.getValidator")
def test_create_empty_object(mock_validator, dao):

    # Arrange
    mock_validator.return_value = {}

    dao.collection.insert_one.side_effect = Exception("WriteError")

    # Act + Assert
    with pytest.raises(Exception):
        dao.create({})


# ==================================================
# TC4: Wrong datatype
# ==================================================

@patch("src.util.dao.getValidator")
def test_create_wrong_datatype(mock_validator, dao):

    # Arrange
    mock_validator.return_value = {}

    dao.collection.insert_one.side_effect = Exception("WriteError")

    # Act + Assert
    with pytest.raises(Exception):
        dao.create({
            "name": 123,
            "active": "yes"
        })


# ==================================================
# TC5: Database failure
# ==================================================

@patch("src.util.dao.getValidator")
def test_create_database_failure(mock_validator, dao):

    # Arrange
    mock_validator.return_value = {}

    dao.collection.insert_one.side_effect = Exception("DB Error")

    # Act + Assert
    with pytest.raises(Exception):
        dao.create({
            "name": "Bob",
            "active": True
        })