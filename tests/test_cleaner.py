import pymongo
import pytest
from mdb_fields_cleaner import Cleaner


@pytest.fixture
def db() -> pytest.fixture():
    client = pymongo.MongoClient()
    return client["test_db"]


def test_main(db):
    expected_deleted = {"color", "year"}
    cleaner = Cleaner(db)
    db.cars.insert_many(
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
    results = cleaner.clean("cars", ["make", "model"])
    assert results
    for doc in db.cars.find({}):
        assert expected_deleted not in set(doc.keys())
