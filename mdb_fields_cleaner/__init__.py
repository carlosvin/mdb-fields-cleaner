from typing import Sequence
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.results import UpdateResult


class Cleaner:
    """
    Helper to easily remove any field from a collection
    """

    def __init__(self, db: MongoClient):
        """
        :db: [MongoClient](https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient)
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
        field_names = set[str]()
        cursor = collection.aggregate([{"$sample": {"size": 1000}}])
        for doc in cursor:
            field_names.update(doc.keys())
        return field_names
