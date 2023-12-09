from typing import Sequence
from pymongo import MongoClient
from pymongo.collection import Collection


class Cleaner:
    def __init__(self, db: MongoClient):
        self.db = db

    def clean(self, collection_name: str, keep_fields: Sequence[str]) -> None:
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
