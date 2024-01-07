import pymongo
import pytest


@pytest.fixture
def db():
    return pymongo.MongoClient().get_database("test_db")


@pytest.fixture
def test_name(request) -> str:
    return request.node.name
