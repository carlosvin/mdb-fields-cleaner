from dataclasses import dataclass
from typing import Type
from pydantic import BaseModel
import pytest
from mdb_fields_cleaner import ModelBasedCleaner

from mdb_fields_cleaner.dataclass import DataClassCleaner
from mdb_fields_cleaner.pydantic import PydanticCleaner


class User(BaseModel):
    name: str
    age: int
    email: str


@dataclass
class UserDC:
    name: str
    age: int
    email: str


@pytest.mark.parametrize(
    "cleaner_class,model",
    (
        [DataClassCleaner, UserDC],
        [PydanticCleaner, User],
        [DataClassCleaner, UserDC(name="Carlos", age=41, email="carlos@test.com")],
        [PydanticCleaner, User(name="Carlos", age=41, email="carlos@test.com")],
    ),
)
def test_cleanup_data_model(cleaner_class: Type[ModelBasedCleaner], model, db, test_name):
    """validate that the data model is cleaned correctly"""
    expected_deleted = {"foo", "bar", "foo.bar"}
    collection = db.get_collection(f"{test_name}_users")
    collection.drop()
    collection.insert_many(
        [
            {
                "name": "Carlos",
                "age": 41,
                "email": "carlos@test.com",
                "foo": "foo",
                "bar": "bar",
            },
            {
                "name": "Lucas",
                "age": 22,
                "email": "lucas@test.com",
            },
            {
                "name": "Pierre",
                "age": 33,
                "email": "pierre@test.com",
                "foo": {"bar": "bar"},
            },
        ]
    )
    cleaner = cleaner_class(db)
    results = cleaner.clean_fields_not_in_model(collection_name=collection.name, class_or_instance=model)
    assert results.modified_count == 2
    for doc in collection.find({}):
        assert expected_deleted.intersection(doc.keys()) == set()
