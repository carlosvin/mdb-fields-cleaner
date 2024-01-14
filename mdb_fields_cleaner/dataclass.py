from dataclasses import fields
from mdb_fields_cleaner import Cleaner, ModelBasedCleaner
from pymongo.results import UpdateResult


class DataClassCleaner(ModelBasedCleaner, Cleaner):
    """
    Helper class to easily remove any field in a collection that is not a field
    in the data class
    """

    def clean_fields_not_in_model(
        self, collection_name: str, class_or_instance
    ) -> UpdateResult:
        """
        Remove any field from a collection that is not a field in the data class
        """
        return super().clean(
            collection_name,
            keep_fields=[field.name for field in fields(class_or_instance)],
        )
