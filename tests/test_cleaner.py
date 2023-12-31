import pymongo
import pytest
from mdb_fields_cleaner import Cleaner


@pytest.fixture
def db():
    return pymongo.MongoClient().get_database("test_db")


@pytest.fixture
def test_name(request) -> str:
    return request.node.name


def test_main(db, test_name):
    expected_deleted = {"color", "year"}
    collection = db.get_collection(f"{test_name}_cars")
    collection.drop()
    cleaner = Cleaner(db)
    collection.insert_many(
        [
            {
                "make": "Ford",
                "model": "Mustang",
                "year": 1964,
                "color": "red",
            },
            {
                "make": "Ford",
                "model": "Escort",
            },
            {
                "make": "Seat",
                "model": "Ibiza",
                "year": 200,
                "color": "green",
            },
        ]
    )
    results = cleaner.clean(collection.name, ["make", "model"])
    assert results.modified_count == 2
    for doc in collection.find({}):
        assert expected_deleted.intersection(doc.keys()) == set()
