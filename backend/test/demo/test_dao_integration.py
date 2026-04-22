import pytest
from unittest.mock import MagicMock
from src.util.dao import DAO


# ------------------------------------------------
# Fixture
# ------------------------------------------------
@pytest.fixture
def dao():
    test_dao = DAO("user")
    test_dao.collection = MagicMock()
    return test_dao


# ------------------------------------------------
# TC1 Valid data -> insert succeeds
# ------------------------------------------------
def test_create_valid_data(dao):
    data = {"name": "Alice", "active": True}

    dao.collection.insert_one.return_value.inserted_id = 1
    dao.collection.find_one.return_value = {"_id": 1, "name": "Alice", "active": True}
    dao.to_json = MagicMock(return_value={"_id": "1", "name": "Alice", "active": True})

    result = dao.create(data)

    assert result["name"] == "Alice"
    assert result["_id"] == "1"


# ------------------------------------------------
# TC2 Missing field / invalid validator
# ------------------------------------------------
def test_create_invalid_data(dao):
    dao.collection.insert_one.side_effect = Exception("WriteError")

    with pytest.raises(Exception):
        dao.create({"name": "OnlyName"})


# ------------------------------------------------
# TC3 Empty object
# ------------------------------------------------
def test_create_empty_object(dao):
    dao.collection.insert_one.side_effect = Exception("WriteError")

    with pytest.raises(Exception):
        dao.create({})


# ------------------------------------------------
# TC4 Wrong datatype
# ------------------------------------------------
def test_create_wrong_datatype(dao):
    dao.collection.insert_one.side_effect = Exception("WriteError")

    with pytest.raises(Exception):
        dao.create({"name": 123, "active": "yes"})


# ------------------------------------------------
# TC5 Database failure
# ------------------------------------------------
def test_create_database_failure(dao):
    dao.collection.insert_one.side_effect = Exception("DB Error")

    with pytest.raises(Exception):
        dao.create({"name": "Bob", "active": True})