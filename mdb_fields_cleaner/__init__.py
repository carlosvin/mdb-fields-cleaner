from abc import ABC, abstractmethod
from typing import Sequence
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import UpdateResult
from pymongo.database import Database


class Cleaner:
    """
    Helper to easily remove any field from a collection
    """

    def __init__(self, db: Database):
        """
        :db: [MongoDB database](https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-database)
        """
        self.db = db

    def clean(self, collection_name: str, keep_fields: Sequence[str]) -> UpdateResult:
        """
        :collection_name: Name of the collection to clean up the fields
        :keep_fields: Sequence of fields that we want to keep in our collection
        """
        collection: Collection = self.db.get_collection(collection_name)
        fields = self.get_field_names(collection)
        fields.difference_update(keep_fields)
        fields.remove("_id")
        return collection.update_many(
            {},
            {"$unset": {field: "" for field in fields}},
        )

    def get_field_names(self, collection: Collection) -> set[str]:
        """
        :collection: The MongoDB collection from where to get the field names
        Returns a set with all the field names in the specified collection
        """
        field_names = set[str]()
        cursor = collection.aggregate([{"$sample": {"size": 1000}}])
        for doc in cursor:
            field_names.update(doc.keys())
        return field_names


class ModelBasedCleaner(ABC):
    """
    Helper to remove any field in the collection that is not defined in the data model
    """

    @abstractmethod
    def clean_fields_not_in_model(
        self, collection_name: str, class_or_instance
    ) -> UpdateResult:
        """
        Remove any field from a collection that is not a field in class model
        """
